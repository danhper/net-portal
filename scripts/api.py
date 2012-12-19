#!/usr/bin/env python2

from http import *
from bs4 import BeautifulSoup

request = HTTPRequest('portal/portal.php', 'https://www.wnp.waseda.jp', encoding='euc-jp')

response = request.send()
cookies = response.get_header('set-cookie')
print cookies


request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
request.add_header('Accept-Encoding', 'gzip, deflate')
request.add_header('Connection', 'keep-alive')
request.add_header('Cookie', response.headers['set-cookie'])

request.add_parameter('JavaCHK', 1)
request.add_parameter('LOGINCHECK', 1)
