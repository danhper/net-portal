from datetime import datetime, timedelta
import re

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
