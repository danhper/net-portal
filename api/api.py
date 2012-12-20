#!/usr/bin/env python2

from http import HTTPRequest
# from bs4 import BeautifulSoup
import login_config

class NetPortalException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NetPortalAPI:
    def __init__(self):
        self.request = HTTPRequest('portal/portal.php', 'https://www.wnp.waseda.jp', encoding='euc-jp')
        self.request.set_dummy_headers()
        self.request.set_parameter('JavaCHK', 1)
        self.request.set_parameter('LOGINCHECK', 1)
        self.request.set_parameter('HID_P14', 'EN')

    def login(self):
        response = self.request.send()
        self.request.set_cookies(response.cookies)
        if not 'PHPSESSID' in response.cookies:
            raise NetPortalException("Could not get PHPSESSID")
        self.request.set_parameter('PHPSESSID', response.cookies['PHPSESSID'].value)
        self.request.url = 'portal/portalLogin.php'
        response = self.request.send()
        self.request.set_cookies(response.cookies)
        if not 'PHP_Sessionid' in response.cookies:
          raise NetPortalException("Could not get PHP_Sessionid")

        self.request.url = 'portal/portal.php'
        self.request.remove_parameter('PHPSESSID')
        self.request.set_parameter('PHP_Sessionid', response.cookies['PHP_Sessionid'].value)
        self.request.set_parameter('loginid', login_config.username)
        self.request.set_parameter('passwd', login_config.password)
        self.request.method = "POST"
        response = self.request.send()
        self.request.set_cookies(response.cookies)

        # print response.get_body()
        # print self.request.cookies

    def login_cnavi(self):
        self.request.base_url = 'https://cnavi.waseda.jp'
        self.request.url = 'coursenavi/index3.php'
        response = self.request.send()

        print response.headers
        print response.get_raw_body().decode('utf-8')  # cant decode ><


if __name__ == '__main__':
    api = NetPortalAPI()
    api.login()
    api.login_cnavi()
