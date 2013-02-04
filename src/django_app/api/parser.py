# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import datetime

class NetPortalParser(object):
    def __init__(self, language):
        self.space = " " if language == "en" else "　"


class CourseNaviParser(NetPortalParser):
    def __init__(self):
        super(NetPortalParser, self).__init__()

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
            'waseda_content_id': content_id,
            'waseda_folder_id': folder_id
        }

    def parse_document_list(self, html):
        soup = BeautifulSoup(html)
        content = soup.find('div', {'id': 'cHonbun'})
        docs = content.find_all('div', {'class': 'ctable-main'})
        documents = []
        for d in docs:
            title = d.h2.find('span', {'class': 'ta1col-left'})['title']
            doctype = 'news' if d.h2['class'][0].endswith('un') else 'notes'
            documents.append({'title': title, 'doctype': doctype, 'documents': []})
            documents_list = d.find('ul')
            if documents_list:
                for li in documents_list.ul('li'):
                    document = self._parse_single_document(li)
                    documents[-1]['documents'].append(document)

        return documents
