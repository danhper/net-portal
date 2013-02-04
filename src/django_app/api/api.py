#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from http import HTTPRequest, URI
from bs4 import BeautifulSoup
import login_config
import re

def parse_name(name, info, prefix, sep):
    last, first = name.split(sep, 1)
    info[prefix + '_first_name'] = first.strip()
    info[prefix + '_last_name'] = last.strip()

info_input = {
    'HID_P4': lambda n, i: parse_name(n, i, 'ja', u'　'),
    'HID_P5': lambda n, i: parse_name(n, i, 'en', ','),
    'HID_P13': lambda n, i: i.update(student_nb=n)
}

subjects_category = {
    'attending': 'list',
    'to_attend': 'before',
    'attended': 'end',
    'favorite': 'favorite'
}

class NetPortalException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NetPortalAPI(object):
    def __init__(self, language="EN"):
        self.request = HTTPRequest(URI('https://www.wnp.waseda.jp/portal', 'portal.php'), encoding='euc-jp')
        self.request.set_dummy_headers()
        self.request.set_parameter('JavaCHK', 1)
        self.request.set_parameter('LOGINCHECK', 1)
        self.language = language
        self.set_language()
        self.logged = False
        self.logged_cnavi = False
        self._user_info = {}
        self.session_id_encode_key = None

    def set_language(self):
        self.request.set_parameter('HID_P14', self.language)

    @property
    def user_info(self):
        if not self.logged:
            raise NetPortalException("Need to login to get user info from API.")
        return self._user_info

    def login(self, username, password):
        self.request.uri.url = 'portal.php'
        self.request.method = "GET"
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

        body = BeautifulSoup(response.get_body())

        # get hidden form with personal info
        form = body.find("form", {'name': 'LinkIndication'})
        self.request.reset_parameters()
        for field in form.find_all("input"):
            self.request.set_parameter(field['name'], field['value'])
            if field['name'] in info_input.keys():
                info_input[field['name']](field['value'], self._user_info)

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
        if not self.logged:
            raise NetPortalException("Need to login before login to cnavi")
        self.request.uri = URI('https://cnavi.waseda.jp', 'coursenavi/index2.php')
        self.request.method = "POST"
        self.request.set_parameters(self.cnavi_data)
        self.request.encoding = "utf-8"
        self.request.remove_cookie("PHPSESSID")  # different PHPSESSID for this domain

        response = self.request.send()
        self.request.set_cookies(response.cookies)
        self.cnavi_data.clear()
        body = BeautifulSoup(response.get_body())

        for field in body.find_all("input"):
            self.cnavi_data[field['name']] = field['value']
        self.request.set_parameters(self.cnavi_data)
        self.request.uri.url = "index.php"

        self.logged_cnavi = True

    def get_all_subjects(self):
        subjects = {}
        for cat in ['attending', 'to_attend', 'attended']:
            subjects.update(self.get_subjects(cat))
        return subjects

    def get_subjects(self, subject_category='attending'):
        if not self.logged_cnavi:
            raise NetPortalException("Need to login to cnavi to get subjects")
        self.request.set_parameter('ControllerParameters', 'ZX14SubCon')
        self.request.set_parameter('hidListMode', subjects_category[subject_category])
        response = self.request.send()
        body = BeautifulSoup(response.get_body())
        subjects_container = body.find('div', {'id': 'wKTable'}).find("ul")
        ids = []
        folders = []
        for subject in subjects_container.find_all("li"):
            info = subject.find('p', {'class': 'w-col6'})
            ids.append(info.find('input', {'name': 'chkbox[]'})['value'])
            folders.append(info.find('input', {'name': 'folder_id[]'})['value'])

        subjects = {}
        # ids are in the form "yyyyIDIDIDID"
        # use IDIDIDID as dictionary key
        # zip with folders to iterate on all needed information
        for (k, y, f) in map(lambda (s, f): (s[4:], s[:4], f), zip(ids, folders)):
            subjects.setdefault(k, {"folder_id": f, "years": []})
            subjects[k]["years"].append(y)

        return subjects

    def get_subject_documents(self, subject_id, subject_folder_id):
        self.request.set_parameter('hidCommunityId', subject_id)
        self.request.set_parameter('hidFolderId', subject_folder_id)
        self.request.set_parameter('ControllerParameters', 'ZX21SubCon')
        self.request.set_parameter('hidListMode', 'list')
        self.request.set_parameter('simpletype', 0)
        self.request.set_parameter('hidCommBcd', '01')
        self.request.set_parameter('hidCommKcd', '01')

        response = self.request.send()
        print response.get_body()
        print response.code

    def get_lecture_documents(self, subject_id, subject_folder_id, doc_id, doc_folder_id):
        self.request.set_parameter('hidCommunityId', subject_id)
        self.request.set_parameter('hidContactFolderId', subject_folder_id)
        self.request.set_parameter('hidContentsId', doc_id)
        self.request.set_parameter('hidFolderId', doc_folder_id)
        self.request.set_parameter('simpletype', 0)
        self.request.set_parameter('hidCommBcd', '01')
        self.request.set_parameter('hidCommKcd', '01')

        if doc_id:
            self.request.set_parameter('hidListMode', 'detail')
            self.request.set_parameter('ControllerParameters', 'ZX31DtlSubCon')
        else:
            self.request.set_parameter('hidListMode', 'list')
            self.request.set_parameter('ControllerParameters', 'ZX21SubCon')

        response = self.request.send()
        print response.get_body()


if __name__ == '__main__':
    api = NetPortalAPI(language='JA')
    api.login(login_config.username, login_config.password)
    api.login_cnavi()
    #print api.get_subjects('attended')
    # api.get_subject_documents('2012260302300501', '1787886')
    # api.get_lecture_documents('2012260302300501', '1787886', '15056275', '1913470')
    # api.get_lecture_documents('2012260302300501', '1787886', '', '1982251')
