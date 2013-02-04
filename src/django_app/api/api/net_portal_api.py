#-*- coding: utf-8 -*-

from ..http import HTTPRequest, URI
from bs4 import BeautifulSoup
from ..parsers import NetPortalParser
from ..exceptions import NetPortalException

class NetPortalAPI(object):
    def __init__(self, language="EN", Parser=NetPortalParser):
        self.request = HTTPRequest(URI('https://www.wnp.waseda.jp/portal', 'portal.php'), encoding='euc-jp')
        self.language = language
        self.logged = False
        self.logged_cnavi = False
        self._user_info = {}
        self.session_id_encode_key = None
        self.parser = Parser(language)
        self._reset_request()
        self.cnavi_data = {}

    def set_language(self):
        self.request.set_parameter('HID_P14', self.language.upper())

    @property
    def user_info(self):
        if not self.logged:
            raise NetPortalException("Need to login to get user info from API.")
        return self._user_info

    def _reset_request(self):
        self.request.reset_parameters()
        self.request.reset_cookies()
        self.set_language()
        self.request.set_parameter('JavaCHK', 1)
        self.request.set_parameter('LOGINCHECK', 1)
        self.request.set_dummy_headers()

    def login(self, username, password):
        if self.logged:
            return True

        self.request.uri.url = 'portal.php'
        self.request.method = "GET"
        response = self.request.send()

        self.request.set_cookies(response.cookies)
        if not self.request.has_cookie('PHPSESSID'):
            raise NetPortalException("Could not get PHPSESSID")
        self.net_portal_sessid = self.request.cookies['PHPSESSID']
        self.request.set_parameter('PHPSESSID', self.request.cookies['PHPSESSID'].value)
        self.request.uri.url = 'portalLogin.php'
        response = self.request.send()

        self.request.set_cookies(response.cookies)
        if not self.request.has_cookie('PHP_Sessionid'):
          raise NetPortalException("Could not get PHP_Sessionid")

        self.request.uri.url = 'portal.php'
        self.request.remove_parameter('PHPSESSID')
        self.request.set_parameter('PHP_Sessionid', self.request.cookies['PHP_Sessionid'].value)
        self.request.set_parameter('loginid', username)
        self.request.set_parameter('passwd', password)
        self.request.method = "POST"
        response = self.request.send()

        # check if password was correct
        if not 'Admission_Key' in response.cookies:
            return False

        self.request.set_cookies(response.cookies)

        body = BeautifulSoup(response.get_body())
        link = body.find("frame", {'name': 'LeftMenu'})['src']
        self._get_left_menu_info(URI.parse(link, is_relative=True))
        self.logged = True
        return True

    def _get_left_menu_info(self, uri):
        # get left menu
        self.request.uri.url = uri.url
        self.request.reset_parameters()
        self.request.method = "GET"
        for (key, value) in uri.params.items():
            self.request.set_parameter(key, value)

        response = self.request.send()
        self.request.set_cookies(response.cookies)

        # parse left menu

        soup = BeautifulSoup(response.get_body())
        self._user_info = self.parser.parse_peronal_info(soup)
        self.cnavi_data = self.parser.parse_cnavi_data(soup)
