#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from net_portal_api import NetPortalAPI
from ..exceptions import NetPortalException
from ..parsers import CourseNaviParser
from ..http import URI

class CourseNaviAPI(NetPortalAPI):
    def __init__(self, language="EN", Parser=CourseNaviParser):
        super(CourseNaviAPI, self).__init__(language, Parser)
        self.subjects_category = {
            'attending': 'list',
            'to_attend': 'before',
            'attended': 'end',
            'favorite': 'favorite'
        }

    def _prepare_cnavi_login(self):
        self.request.set_parameters(self.cnavi_data)

        self.request.uri.url = "LogOutput.php"
        self.request.method = "POST"
        response = self.request.send()

        # prepare data to log to course navi
        self.request.set_cookies(response.cookies)
        body = BeautifulSoup(response.get_body())

        for field in body.find_all("input"):
            self.cnavi_data[field['name']] = field['value']

    def login_cnavi(self):
        if not self.logged:
            raise NetPortalException("Need to login before login to cnavi")

        self._prepare_cnavi_login()
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
        for category in ['attending', 'to_attend', 'attended']:
            subjects.update(self.get_subjects(category))
        return subjects

    def get_subjects(self, subject_category='attending'):
        if not self.logged_cnavi:
            raise NetPortalException("Need to login to cnavi to get subjects")
        self.request.set_parameter('ControllerParameters', 'ZX14SubCon')
        self.request.set_parameter('hidListMode', self.subjects_category[subject_category])
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
