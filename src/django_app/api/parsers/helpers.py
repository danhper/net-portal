from bs4 import BeautifulSoup

def souped(f):
    def wrapper(instance, html):
        body = html if type(html) == BeautifulSoup else BeautifulSoup(html)
        return f(instance, body)
    return wrapper
