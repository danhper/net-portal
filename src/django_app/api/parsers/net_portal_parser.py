# -*- coding: utf-8 -*-

import re
from ..exceptions import NetPortalException
from helpers import souped

class NetPortalParser(object):
    def __init__(self, language):
        self.space = " " if language == "en" else "　"

    def _parse_name(self, name, sep):
        last, first = name.split(sep, 1)
        return (first.strip(), last.strip())

    @souped
    def parse_peronal_info(self, html):
        form = html.find("form", {'name': 'LinkIndication'})
        user_info = {}
        for field in form.find_all("input"):
            if field['name'] == 'HID_P4':
                first_name, last_name = self._parse_name(field['value'], u'　')
                user_info['ja_first_name'], user_info['ja_last_name'] = first_name, last_name
            elif field['name'] == 'HID_P5':
                first_name, last_name = self._parse_name(field['value'], ',')
                user_info['en_first_name'], user_info['en_last_name'] = first_name, last_name
            elif field['name'] == 'HID_P13':
                user_info['student_nb'] = field['value']
        return user_info

    @souped
    def parse_cnavi_data(self, html):
        form = html.find("form", {'name': 'LinkIndication'})
        parameters = {}
        for field in form.find_all("input"):
            parameters[field['name']] = field['value']

        # get missing info from JS
        missing_info = ["LinkURL", "CateCode", "MenuCode", "UrlCode", "LogData", "MenuLinkName"]
        reg = ".*?MenuLinkOpen\(" + ("\'(.*?)\'," * 5) + "\'(.*?)\'\).*"  # regex for JS function call params -_-'
        # info written in the last script of the first table

        target_script = html.find("table").find_all("script")[-1]
        for line in str(target_script).splitlines():
            if "coursenavi/index3.php" in line:
                m = re.match(reg, line)
                if not m:
                    raise NetPortalException("Could not parse course navi link")
                # missing info captured in groups 1 to 6
                for (key, value) in zip(missing_info, [m.group(i) for i in range(1, 7)]):
                    parameters[key.decode("utf-8")] = value.decode("utf-8")  # BeautifulSoup encodes in utf by default
                break
        return parameters
