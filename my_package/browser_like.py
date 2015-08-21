import urllib.request
import http.cookiejar
import re

# header: dict of header
header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'zh-CN',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
def makeMyOpener(head):
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
def return_data(url):
    my_opener = makeMyOpener(header)
    user_response = my_opener.open(url, timeout = 1000)
    data = user_response.read()
    return data.decode('utf-8')

def return_response(url):    
    my_opener = makeMyOpener(header)
    user_response = my_opener.open(url, timeout = 1000)
    return user_response