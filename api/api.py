#!/usr/bin/env python2

from http import HTTPRequest
# from bs4 import BeautifulSoup

class NetPortalException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class NetPortalAPI:
  def __init__(self):
    self.request = HTTPRequest('portal/portal.php', 'https://www.wnp.waseda.jp', encoding='euc-jp')
    self.request.set_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    self.request.set_header('Accept-Encoding', 'gzip, deflate')
    self.request.set_header('Connection', 'keep-alive')
    self.request.set_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0')
    self.request.set_header('Referer', 'https://www.wnp.waseda.jp/portal/portalLogin.php?ERRFLAG=1&LoginID=&HID_P14=EN&loginFormDisabled=')
    self.request.set_header('Host', 'www.wnp.waseda.jp')
    self.request.set_parameter('JavaCHK', 1)
    self.request.set_parameter('LOGINCHECK', 1)
    self.request.set_parameter('HID_P14', 'EN')

  def login(self):
    response = self.request.send()
    self.request.set_cookies(response.cookies)
    if not 'PHPSESSID' in response.cookies:
      raise NetPortalException("Could not get PHPSESSID")
    self.request.set_parameter('PHPSESSID', response.cookies['PHPSESSID'].value)
    self.request.set_url('portal/portalLogin.php')
    response = self.request.send()
    self.request.set_cookies(response.cookies)
    if not 'PHP_Sessionid' in response.cookies:
      raise NetPortalException("Could not get PHP_Sessionid")

    self.request.set_url('portal/portal.php')
    self.request.remove_parameter('PHPSESSID')
    self.request.set_parameter('PHP_Sessionid', response.cookies['PHP_Sessionid'].value)
    self.request.set_parameter('loginid', 'email here')
    self.request.set_parameter('passwd', 'password here')
    self.request.method = "POST"
    response = self.request.send()

    print(response.get_body())


if __name__ == '__main__':
  api = NetPortalAPI()
  api.login()
