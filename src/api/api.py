#!/usr/bin/env python2

from http import HTTPRequest, URI
from bs4 import BeautifulSoup
import login_config
import re

class NetPortalException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NetPortalAPI:
    def __init__(self, language="EN"):
        self.request = HTTPRequest(URI('https://www.wnp.waseda.jp/portal', 'portal.php'), encoding='euc-jp')
        self.request.set_dummy_headers()
        self.request.set_parameter('JavaCHK', 1)
        self.request.set_parameter('LOGINCHECK', 1)
        self.language = language
        self.set_language()

    def set_language(self):
        self.request.set_parameter('HID_P14', self.language)

    def login(self):
        response = self.request.send()
        self.request.set_cookies(response.cookies)
        if not 'PHPSESSID' in response.cookies:
            raise NetPortalException("Could not get PHPSESSID")
        self.net_portal_sessid = response.cookies['PHPSESSID']
        self.request.set_parameter('PHPSESSID', response.cookies['PHPSESSID'].value)
        self.request.uri.url = 'portalLogin.php'
        response = self.request.send()
        self.request.set_cookies(response.cookies)
        if not 'PHP_Sessionid' in response.cookies:
          raise NetPortalException("Could not get PHP_Sessionid")

        self.request.uri.url = 'portal.php'
        self.request.remove_parameter('PHPSESSID')
        self.request.set_parameter('PHP_Sessionid', response.cookies['PHP_Sessionid'].value)
        self.request.set_parameter('loginid', login_config.username)
        self.request.set_parameter('passwd', login_config.password)
        self.request.method = "POST"
        response = self.request.send()
        self.request.set_cookies(response.cookies)

        body = BeautifulSoup(response.get_body())
        link = body.find("frame", {'name': 'LeftMenu'})['src']
        self.get_left_menu_info(URI.parse(link, is_relative=True))

    def get_left_menu_info(self, uri):
        # get left menu
        self.request.uri.url = uri.url
        self.request.reset_parameters()
        self.request.method = "GET"
        for (key, value) in uri.params.items():
            self.request.set_parameter(key, value)

        response = self.request.send()
        self.request.set_cookies(response.cookies)

        # parse left menu

        body = BeautifulSoup(response.get_body())

        # get hidden form with personal info
        form = body.find("form", {'name': 'LinkIndication'})
        self.request.reset_parameters()
        for field in form.find_all("input"):
            self.request.set_parameter(field['name'], field['value'])

        # get missing info from JS
        missing_info = ["LinkURL", "CateCode", "MenuCode", "UrlCode", "LogData", "MenuLinkName"]
        reg = ".*?MenuLinkOpen\(" + ("\'(.*?)\'," * 5) + "\'(.*?)\'\).*"  # regex for JS function call params -_-'
        # info written in the last script of the first table

        target_script = body.find("table").find_all("script")[-1]
        for line in str(target_script).splitlines():
            if "coursenavi/index3.php" in line:
                m = re.match(reg, line)
                if not m:
                    raise NetPortalException("Could not parse course navi link")
                # missing info captured in groups 1 to 6
                for (key, value) in zip(missing_info, [m.group(i) for i in range(1, 7)]):
                    self.request.set_parameter(key.decode("utf-8"), value.decode("utf-8"))  # BeautifulSoup encodes in utf by default
                break

        self.request.uri.url = "LogOutput.php"
        self.request.method = "POST"
        response = self.request.send()

        # prepare data to log to course navi
        self.request.set_cookies(response.cookies)
        body = BeautifulSoup(response.get_body())
        self.cnavi_data = {}
        for field in body.find_all("input"):
            self.cnavi_data[field['name']] = field['value']

    def login_cnavi(self):
        self.request.uri = URI('https://cnavi.waseda.jp', 'coursenavi/index3.php')
        self.request.method = "POST"
        self.request.set_parameters(self.cnavi_data)
        self.request.encoding = "utf-8"
        self.request.remove_cookie("PHPSESSID")  # different PHPSESSID for this domain

        response = self.request.send()
        self.request.set_cookies(response.cookies)
        body = BeautifulSoup(response.get_body())

        for field in body.find_all("input"):
            self.cnavi_data[field['name']] = field['value']
        self.request.set_parameters(self.cnavi_data)
        self.request.uri.url = "coursenavi/index2.php"

        response = self.request.send()
        self.request.set_cookies(response.cookies)
        self.cnavi_data.clear()
        body = BeautifulSoup(response.get_body())

        for field in body.find_all("input"):
            self.cnavi_data[field['name']] = field['value']
        self.request.set_parameters(self.cnavi_data)
        self.request.uri.url = "index.php"

        response = self.request.send()

        body = BeautifulSoup(response.get_body())

        for field in body.find_all("input"):
            self.cnavi_data[field['name']] = field['value']

    def get_subjects(self):
        self.request.set_parameters(self.cnavi_data)

        response = self.request.send()
        body = BeautifulSoup(response.get_body())
        subjects = body.find('div', {'id': 'wKTable'}).find("ul")
        for subject in subjects.find_all("li"):
            info = subject.find('p', {'class': 'w-col6'})
            print info.find('input', {'name': 'community_name[]'})['value']

if __name__ == '__main__':
    api = NetPortalAPI(language='JA')
    api.login()
    api.login_cnavi()
    api.get_subjects()
