#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from net_portal_api import NetPortalAPI
from ..exceptions import NetPortalException
from ..parsers import CourseNaviParser
from ..http import URI

class CourseNaviAPI(NetPortalAPI):
    def __init__(self, language="EN", Parser=CourseNaviParser):
        super(CourseNaviAPI, self).__init__(language, Parser)
        self._subjects_category = {
            'attending': 'list',
            'to_attend': 'before',
            'attended': 'end',
            'favorite': 'favorite'
        }

    def _get_cnavi_uri(self, page=''):
        return URI('https://cnavi.waseda.jp', page)

    def _prepare_cnavi_portal_login(self):
        self.request.set_parameters(self.cnavi_data)

        self.request.uri.url = "LogOutput.php"
        self.request.method = "POST"
        response = self.request.send()

        # prepare data to log to course navi
        self.request.set_cookies(response.cookies)
        body = BeautifulSoup(response.get_body())

        for field in body.find_all("input"):
            self.cnavi_data[field['name']] = field['value']

    def _cnavi_direct_login(self, username, password):
        self.request.method = "GET"
        self.request.uri = self._get_cnavi_uri()
        self.request.encoding = "utf-8"
        response = self.request.send()
        self.request.set_cookies(response.cookies)
        for field in BeautifulSoup(response.get_body())('input', {'type': 'hidden'}):
            self.request.set_parameter(field['name'], field['value'])
        self.request.set_parameter('id', username)
        self.request.set_parameter('password', password)
        self.request.set_parameter("vertype", "1")
        self.request.method = "POST"
        response = self.request.send()
        body = BeautifulSoup(response.get_body())
        logged = not bool(body.find('p', {'class': 'f-red'}))
        return (logged, body)

    def _cnavi_portal_login(self):
        self._prepare_cnavi_portal_login()
        self.request.uri = self._get_cnavi_uri('coursenavi/index2.php')
        self.request.remove_cookie("PHPSESSID")  # different PHPSESSID for this domain
        self.request.encoding = "utf-8"
        self.request.method = "POST"
        self.request.set_parameters(self.cnavi_data)
        response = self.request.send()
        self.request.set_cookies(response.cookies)
        self.cnavi_data.clear()
        return BeautifulSoup(response.get_body())

    def login_cnavi(self, username=None, password=None):
        if not self.logged:
            if not (username and password):
                raise NetPortalException("Need username/password, or to be logged in to login to cnavi")
            (logged, prelogin_page) = self._cnavi_direct_login(username, password)
            if not logged:
                return False
        else:
            prelogin_page = self._cnavi_portal_login()

        for field in prelogin_page.find_all("input"):
            self.cnavi_data[field['name']] = field['value']
        self.request.set_parameters(self.cnavi_data)
        self.request.uri.url = "index.php"

        self.logged_cnavi = True

        return True

    def get_all_subjects(self):
        subjects = {}
        for category in ['attending', 'to_attend', 'attended']:
            subjects.update(self.get_subjects(category))
        return subjects

    def get_subjects(self, subject_category='attending'):
        if not self.logged_cnavi:
            raise NetPortalException("Need to login to cnavi to get subjects")
        if subject_category == 'all':
            return self.get_all_subjects()
        self.request.set_parameter('ControllerParameters', 'ZX14SubCon')
        self.request.set_parameter('hidListMode', self._subjects_category[subject_category])
        response = self.request.send()
        return self.parser.parse_subjects(response.get_body())

    def set_documents_common_params(self):
        self.request.set_parameter('simpletype', 0)
        self.request.set_parameter('hidCommBcd', '01')
        self.request.set_parameter('hidCommKcd', '01')
        self.request.set_parameter('ControllerParameters', 'ZX21SubCon')
        self.request.set_parameter('hidListMode', 'list')

    def get_subject_documents(self, subject_id, subject_folder_id):
        self.request.set_parameter('hidCommunityId', subject_id)
        self.request.set_parameter('hidFolderId', subject_folder_id)
        self.set_documents_common_params()

        response = self.request.send()
        return self.parser.parse_document_list(response.get_body())

    # checking for data
    def get_file(self, year, subject_id, folder_id, contact_folder_id):
        self.set_documents_common_params()
        self.request.set_parameter('hidCurrentViewID', 'ZX21SubCon')
        self.request.set_parameter('ControllerParameters', 'ZZ921DtlSubcon')
        self.request.set_parameter('hidCommunityId', str(year) + subject_id)
        self.request.set_parameter('hidFolderId', folder_id)
        self.request.set_parameter('hidContactFolderId', contact_folder_id)
        self.request.set_parameter('hidContactFunTypeCd', '10101')
        self.request.set_parameter('hidSelectList', 'ZX21')
        self.request.set_parameter('hidDisplayNone', 'none')
        self.request.set_parameter('hidInputMode', 'new')
        self.request.set_parameter('hidFileId', '1925126_1')
        response = self.request.send()
        with open('test_file', 'w') as f:
            f.write(response.get_gunzipped_body())

    # checking for data
    def get_submitted_file(self, year, subject_id, folder_id, contact_folder_id, content_id, file_id):
        self.set_documents_common_params()
        self.request.set_parameter('hidCurrentViewID', 'ZX21SubCon')
        self.request.set_parameter('ControllerParameters', 'ZZ922DtlSubcon')
        self.request.set_parameter('hidCommunityId', str(year) + subject_id)
        self.request.set_parameter('hidFolderId', folder_id)
        self.request.set_parameter('hidContactFolderId', contact_folder_id)
        self.request.set_parameter('hidContactFunTypeCd', '20502')
        self.request.set_parameter('hidSelectList', 'ZX21')
        self.request.set_parameter('hidContentsId', content_id)
        self.request.set_parameter('hidDisplayNone', 'none')
        self.request.set_parameter('hidKamokuId', 'JA81')
        self.request.set_parameter('hidInputMode', 'new')
        self.request.set_parameter('hidFileId', file_id)
        self.request.set_parameter('hidOpenReport', 'list')
        response = self.request.send()
        if response.has_header('Content-Disposition'):
            filename = response.get_header('Content-Disposition').split("'")[-1]
            with open(filename, 'w') as f:
                f.write(response.get_gunzipped_body())

    def get_lecture_documents(self, subject_id, subject_folder_id, doc_id, doc_folder_id):
        self.request.set_parameter('hidCommunityId', subject_id)
        self.request.set_parameter('hidContactFolderId', subject_folder_id)
        self.request.set_parameter('hidContentsId', doc_id)
        self.request.set_parameter('hidFolderId', doc_folder_id)
        self.set_documents_common_params()

        if doc_id:
            self.request.set_parameter('hidListMode', 'detail')
            self.request.set_parameter('ControllerParameters', 'ZX31DtlSubCon')

        response = self.request.send()
        print response.get_body()
