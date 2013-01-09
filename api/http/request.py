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
