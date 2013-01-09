from cookie import Cookie
from StringIO import StringIO
import gzip

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
