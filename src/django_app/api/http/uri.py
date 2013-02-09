import re
from urllib import urlencode

class URI(object):
    def __init__(self, base_url, url='', params={}):
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
