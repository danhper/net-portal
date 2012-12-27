import json
from urllib2 import Request, urlopen, HTTPError, URLError
from urllib import urlencode
from datetime import datetime, timedelta
import re
from StringIO import StringIO
import gzip

__all__ = ['HTTPException', 'HTTPRequest', 'HTTPResponse']

class HTTPException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HTTPRequest(object):
    accepted_methods = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self, uri, encoding='utf-8', method='GET', is_json=False, required_params=[]):
        self.uri = uri
        self.encoding = encoding
        self.method = method
        self.headers = {}
        self.data = {}
        self.sends_json = is_json
        self.receives_json = is_json
        self.required_params = required_params
        self.cookies = {}

    def set_header(self, name, value):
        self.headers[name] = value

    def remove_header(self, name):
        del self.headers[name]

    def set_parameter(self, name, value):
        self.data[name] = value

    def add_parameters(self, params):
        self.data.update(params)

    def set_parameters(self, params):
        self.data = params

    def remove_parameter(self, name):
        del self.data[name]

    def reset_parameters(self):
        self.data = {}

    def set_send_receive_json(self):
        self.set_send_json()
        self.set_receive_json()

    def set_cookie(self, cookie):
        self.cookies[cookie.key] = cookie

    def set_cookies(self, cookies):
        for cookie in cookies.values():
            self.cookies[cookie.key] = cookie

    def remove_cookie(self, key):
        del self.cookies[key]

    def set_send_json(self):
        if self.method not in ["PUT", "POST"]:
            self._method = "POST"
        self.sends_json = True
        self.headers["Content-Type"] = "application/json"

    def set_receive_json(self):
        self.headers["Accept"] = "application/json"
        self.receives_json = True

    def set_dummy_headers(self):
        self.set_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        self.set_header('Accept-Encoding', 'gzip, deflate')
        self.set_header('Connection', 'keep-alive')
        self.set_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0')

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, method):
        method = method.upper()
        if method not in HTTPRequest.accepted_methods:
            raise HTTPException("Unknown HTTP method {0}".format(method))
        self._method = method

    def _prepare_cookies(self):
        if self.cookies:
            self.set_header('Cookie', '; '.join(map(str, self.cookies.values())))

    def check_request(self):
        if any(key not in self.data.keys() for key in self.required_params):
            params_list = ','.join(self.required_params)
            raise HTTPException("Needs parameters '%s'.".format(params_list))

    def make_request(self):
        self.check_request()
        self._prepare_cookies()
        uri = self.uri.with_params(self.encoded_data) if self.method in ["GET", "DELETE"] else str(self.uri)
        request = Request(uri, headers=self.headers)
        request.get_method = lambda: self.method
        if self.method in ["POST", "PUT"]:
            data = json.dumps(self.encoded_data).encode() if self.sends_json else urlencode(self.encoded_data)
            request.add_data(bytes(data.encode(self.encoding)))
        return request

    @property
    def encoded_data(self):
        data = {}
        for (k, v) in self.data.items():
            key = k.encode(self.encoding) if hasattr(k, 'encode') else k
            val = v.encode(self.encoding) if hasattr(v, 'encode') else v
            data[key] = val
        return data

    def send(self):
        request = self.make_request()
        try:
            response = urlopen(request)
            return HTTPResponse(response, encoding=self.encoding, is_json=self.receives_json)
        except URLError as e:
            if e.code == 401:
                raise HTTPException("Error while authenticating.")
            elif e.code == 404:
                raise HTTPException("Page '{0}' does not exist.".format(request.get_full_url()))
            else:
                raise HTTPException("An error has occured: {0}".format(e.code))

class HTTPResponse:
    def __init__(self, response, encoding='utf-8', is_json=False):
        self.is_json = is_json
        self.encoding = encoding
        self._headers = {a.lower(): b for (a, b) in response.info().items()}
        self.cookies = Cookie.parse_cookies(self._headers.get('set-cookie', ''))
        self.raw_body = response.read()
        self.code = response.code
        response.close()

    def get_header(self, header):
        return self._headers[header.lower()]

    @property
    def headers(self):
        return self._headers

    def has_header(self, header):
        return header.lower() in self.headers

    def get_raw_body(self):
        return self.raw_body

    def get_gunzipped_body(self):
        if self.headers.get('content-encoding', '') == 'gzip':
            buf = StringIO(self.get_raw_body())
            f = gzip.GzipFile(fileobj=buf)
            body = f.read()
        else:
            body = self.get_raw_body()
        return body

    def get_body(self):
        body = self.get_gunzipped_body().decode(self.encoding)
        if self.is_json:
            body = json.load(body)
        return body

class URI(object):
    def __init__(self, base_url, url, params={}):
        self.base_url = base_url
        self.url = url
        self.params = params

    def __str__(self):
        return self.base_url + self.url

    def __repr__(self):
        return str(self)

    def with_params(self, params):
        return str(self) + "?" + urlencode(params)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value if value.endswith('/') else value + '/'

    @staticmethod
    def parse(uri, is_relative=False):
        maybe_prot = "(?:(?:https|ftp|file)://)?"
        auth_chars = "[0-9a-zA-Z_-]"
        base_url_format = "{maybe_prot}(?:{auth_chars}+\.)+{auth_chars}{{2,3}}/?"
        base_url = base_url_format.format(maybe_prot=maybe_prot, auth_chars=auth_chars)
        url = "(.*?)"
        params = "(?:\?(.*))"
        if is_relative:
            regex = "{url}{params}".format(base=base_url, url=url, params=params)
        else:
            regex = "({base}){url}{params}".format(base=base_url, url=url, params=params)
        m = re.match(regex, uri)
        if is_relative:
            (base, url, p) = ('', m.group(1).lstrip(".").lstrip("/"), m.group(2))
        else:
            (base, url, p) = (m.group(1), m.group(2), m.group(3))

        params = {k:v for (k,v) in [e.split("=") for e in p.split("&")]} if p else {}

        return URI(base, url, params)


class Cookie(object):
    def __init__(self, key, value, path="/", expire_days=365, domain=None):
        self.key = key
        self.value = value
        self.path = path
        self.expires = self._get_expire(expire_days)
        self.domain = domain

    def _get_expire(self, days):
        max_age = days * 24 * 3600
        return datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

    def __str__(self):
        return '{0}={1}'.format(self.key, self.value)

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse_cookie(cookie):
        cookie = cookie.strip()
        data = cookie.split(";")
        try:
            key, value = map(lambda s: s.strip(), data[0].split("="))
        except ValueError:
            return None
        cookie_object = Cookie(key, value)
        for attribute in data[1:]:
            key, value = map(lambda s: s.strip(), attribute.split('='))
            setattr(cookie_object, key, value)
        return cookie_object

    @staticmethod
    def parse_cookies(cookies_string):
        cookies = {}
        for cookie in re.split('(?<!(day)),', cookies_string):
            if cookie:
                cookie_object = Cookie.parse_cookie(cookie)
                if cookie_object:
                    cookies[cookie_object.key] = cookie_object
        return cookies
