# -*- coding: utf-8 -*-

import re
import datetime
from net_portal_parser import NetPortalParser
from helpers import souped

class CourseNaviParser(NetPortalParser):
    def __init__(self, language):
        super(CourseNaviParser, self).__init__(language)

    @souped
    def parse_subjects(self, html):
        subjects_container = html.find('div', {'id': 'wKTable'}).find("ul")
        ids, folders = [], []
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

    def _parse_display_period(self, period_text):
        date_time_reg = '(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2})'
        m = re.match(".*?{0}.*?{0}.*".format(date_time_reg), period_text.replace("\n", ""))
        start_date = datetime.datetime(*map(int, m.groups()[:5]))
        end_date = datetime.datetime(*map(int, m.groups()[5:]))
        return (start_date, end_date)

    def _parse_waseda_info(self, info_text):
        reg = "post_submit\('.*?','(.*?)','(.*?)',.*?\);"
        m = re.match(reg, info_text)
        return (m.group(2), m.group(1))

    def _parse_single_document(self, content):
        title_info = content.find('span', {'class': 'ta1col-left'})
        title = title_info['title']
        (content_id, folder_id) = self._parse_waseda_info(title_info.a['onclick'])

        info = content.find('span', {'class': 'ta1col-right'})('span')
        last_name, first_name = re.split(u"[　 ]", info[0].text.strip(), 1)

        (start_date, end_date) = self._parse_display_period(info[1].text)

        return {
            'title': title,
            'display_start': start_date,
            'display_end': end_date,
            'uploader': (last_name, first_name),
            'waseda_id': content_id,
        }

    def _parse_document_folder(self, content):
        left_col = content.h2.find('span', {'class': 'ta1col-left'})
        reg = "post_submit\('.*?','(.*?)',.*?\);"
        title = left_col['title']
        waseda_id = re.match(reg, left_col.a['onclick']).group(1)
        doctype = 'news' if content.h2['class'][0].endswith('un') else 'notes'
        return {
            'title': title,
            'waseda_id': waseda_id,
            'doctype': doctype,
            'documents': []
        }

    @souped
    def parse_document_list(self, html):
        content = html.find('div', {'id': 'cHonbun'})
        docs = content.find_all('div', {'class': 'ctable-main'})
        documents = []
        for d in docs:
            documents.append(self._parse_document_folder(d))
            documents_list = d.find('ul')
            if documents_list:
                for li in documents_list.ul('li'):
                    document = self._parse_single_document(li)
                    documents[-1]['documents'].append(document)

        return documents
