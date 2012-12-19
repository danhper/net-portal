import json
from urllib2 import Request, urlopen, HTTPError
from urllib import urlencode
from datetime import datetime, timedelta

__all__ = ['HTTPException', 'HTTPRequest', 'HTTPResponse']

class HTTPException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class HTTPRequest:
    accepted_methods = ["GET", "POST", "PUT", "DELETE"]

    def __init__(self, url, base_url, encoding='utf-8', method='GET', is_json=False, required_params=[]):
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.set_url(url)
        self.encoding = encoding
        self.method = method
        self.headers = {}
        self.datas = {}
        self.sends_json = is_json
        self.receives_json = is_json
        self.required_params = required_params

    def add_header(self, name, value):
        self.headers[name] = value

    def add_parameter(self, name, value):
        self.datas[name] = value

    def add_parameters(self, params):
        self.datas.update(params)

    def set_send_receive_json(self):
        self.set_send_json()
        self.set_receive_json()

    def set_send_json(self):
        if self.method not in ["PUT", "POST"]:
            self._method = "POST"
        self.sends_json = True
        self.headers["Content-Type"] = "application/json"

    def set_receive_json(self):
        self.headers["Accept"] = "application/json"
        self.receives_json = True

    def get_method(self):
        return self._method

    def set_url(self, url):
        self.url = self.base_url + url

    def set_method(self, method):
        method = method.upper()
        if method not in HTTPRequest.accepted_methods:
            raise HTTPException("Unknown HTTP method {0}".format(method))
        self._method = method

    def check_request(self):
        if any(key not in self.datas.keys() for key in self.required_params):
            params_list = ','.join(self.required_params)
            raise HTTPException("Needs parameters '%s'.".format(params_list))

    def make_request(self):
        self.check_request()
        url = self.url
        if self.method in ["GET", "DELETE"] and self.datas:
            q = urlencode(self.datas)
            url += "?" + q
        request = Request(url, headers=self.headers)
        request.get_method = lambda: self.method
        if self.method in ["POST", "PUT"]:
            data = json.dumps(self.datas).encode() if self.sends_json else urlencode(self.datas)
            request.add_data(bytes(data.encode(self.encoding)))
        return request

    def send(self):
        request = self.make_request()
        try:
            response = urlopen(request)
            return HTTPResponse(response, encoding=self.encoding, is_json=self.receives_json)
        except HTTPError as e:
            if e.code == 401:
                raise HTTPException("Error while authenticating.")
            elif e.code == 404:
                raise HTTPException("Page does not exist.")
            else:
                raise HTTPException("An error has occured.")

    method = property(get_method, set_method)


class HTTPResponse:
    def __init__(self, response_file, encoding='utf-8', is_json=False):
        self.response = response_file
        self.is_json = is_json
        self.encoding = encoding
        self._headers = dict(self.response.info().items())

    def get_header(self, header):
        return self._headers[header]

    def get_headers(self):
        return self._headers

    def has_header(self, header):
        return header in self.headers

    def get_body(self):
        body = self.response.read().decode(self.encoding)
        if self.is_json:
            body = json.load(body)
        return body

    headers = property(get_headers, None)

class Cookie:
    def __init__(self, key, value, path="/", expire_days=365):
        self.key = key
        self.value = value
        self.path = path
        self.expire = self._get_expire(expire_days)

    @staticmethod
    def parse_cookie(cookie):
        cookie = cookie.strip()
        pass

    @staticmethod
    def parse_cookies(cookies):
        return [Cookie.parse_cookie(cookie) for cookie in cookies.split(';')]

    def _get_expire(self, days):
        max_age = days * 24 * 3600
        return datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
