import urllib.request
import http.cookiejar
import re

# head: dict of header
def makeMyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'zh-CN',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }):
    cookie_jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
def return_data(url):
    my_opener = makeMyOpener()
    user_response = my_opener.open(url, timeout = 1000)
    data = user_response.read()
    return data.decode('utf-8')

def return_response(url):    
    my_opener = makeMyOpener()
    user_response = my_opener.open(url, timeout = 1000)
    return user_response

# # url = 'http://www.douban.com/accounts/login?source=movie'
# url = 'http://movie.douban.com/'
# data = return_data(url)
# # print(data)

# link_regex = re.compile('(href="http://movie\.douban\.com/subject/(?!\d+/cinema)(.+?)")')
# # print(link_regex)
# for key, value in link_regex.findall(data):
#     # if 'http' in link and link not in visited:
#     #     queue.append(link)
#     #     print('加入队列 --->  ' + link)
#     print(key, value)

# s = link_regex.findall(data)
# print(s)