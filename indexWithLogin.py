import re
import http.cookiejar
import urllib
import urllib.request

def getOpener(head):
	# deal with the Cookies
	cookieJar = http.cookiejar.CookieJar()
	processor = urllib.request.HTTPCookieProcessor(cookieJar)
	opener = urllib.request.build_opener(processor)
	header = []
	for key, value in head.items():
		elem = (key, value)
		header.append(elem)
	opener.addheaders = header
	return opener

header = {
	'POST': '/login HTTP/1.1',
	'Accept': 'text/html, application/xhtml+xml, */*',
	'Referer': 'https://accounts.douban.com/login?source=movie',
	'Accept-Language': 'zh-CN',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Content-Type': 'application/x-www-form-urlencoded',
	# 'Accept-Encoding': 'gzip, deflate',
	'Host': 'accounts.douban.com',
	# 'Content-Length': '130',
	'Connection': 'Keep-Alive',
	'Cache-Control': 'no-cache',
	'Cookie': 'bid="akJS9/utBAM"; viewed="6235530"; ps=y; ll="118104"; ap=1; ue="1074976039@qq.com"; push_noty_num=0; push_doumail_num=0; as="https://movie.douban.com/"',
}

def return_data(url):
    my_opener = getOpener(header)
    user_response = my_opener.open(url, timeout = 1000)
    data = user_response.read()
    return data.decode('utf-8')

url = 'http://www.douban.com/accounts/login?source=movie'
print(return_data(url))
opener = getOpener(header)
op = opener.open(url)
data = op.read()
print(data.decode())
print(data.decode())
 
url += 'login?source=movie'
id = '1074976039@qq.com'
password = '3.1415926'
postDict = {
	'source': 'movie',
	'redir': 'http://movie.douban.com/',
	'form_email': '1074976039@qq.com',
	'form_password': '3.1415926',
	'login': '登录'
}

postData = urllib.parse.urlencode(postDict).encode()
print(postData)
op = opener.open(url, postData)
data = op.read()
# data = ungzip(data)
 
print(data.decode())