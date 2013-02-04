from http_exception import HTTPException
from urllib2 import Request, urlopen, URLError
from urllib import urlencode
from http_response import HTTPResponse
from types import MimeType
import json

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
        self.multipart_form = None
        self.content_type = MimeType.FORM

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

    def has_cookie(self, cookie_name):
        return cookie_name in self.cookies

    def set_cookie(self, cookie):
        self.cookies[cookie.key] = cookie

    def set_cookies(self, cookies):
        for cookie in cookies.values():
            self.cookies[cookie.key] = cookie

    def remove_cookie(self, key):
        del self.cookies[key]

    def reset_cookies(self):
        self.cookies = {}

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

    def _prepare_content_type(self):
        if self.content_type == MimeType.MULTIPART_FORM:
            if not self.multipart_form:
                raise HTTPException("Multipart form must be set when using multipart form content type.")
                self.set_header("Content-type", self.multipart_form.get_content_type())
        else:
            self.set_header("Content-type", self.content_type)

    def check_request(self):
        if any(key not in self.data.keys() for key in self.required_params):
            params_list = ','.join(self.required_params)
            raise HTTPException("Needs parameters '%s'.".format(params_list))

    def get_uri(self):
        if self.method in ["GET", "DELETE"]:
            return self.uri.with_params(self.encoded_data)
        else:
            return str(self.uri)

    def _make_data(self):
        if self.content_type == MimeType.JSON:
            data = json.dumps(self.encoded_data)
        elif self.content_type == MimeType.FORM:
            data = urlencode(self.encoded_data)
        elif self.content_type == MimeType.MULTIPART_FORM:
            data = str(self.multipart_form)
        else:
            raise HTTPException("Content type {0} is not handled".format(self.content_type))
        return bytes(data.encode(self.encoding))

    def _make_request(self):
        self.check_request()
        self._prepare_cookies()
        self._prepare_content_type()
        uri = self.get_uri()
        request = Request(uri, headers=self.headers)
        request.get_method = lambda: self.method
        if self.method in ["POST", "PUT"]:
            request.add_data(self._make_data())
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
        request = self._make_request()
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
