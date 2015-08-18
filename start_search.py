import re
import urllib
import urllib.request
import time

from collections import deque

from my_package import browser_like
from my_package import file_ope

# 待访问的集合queue
queue = deque()
# 访问过的集合visited
visited = set()

# 入口页面
url_start = "http://movie.douban.com/"

queue.append(url_start)
# 已经抓取的页面数count
count = 0

# 当待访问页面不为空时，一直循环
while queue and count <= 1000:
	# 休眠1秒
	time.sleep(1)

	url = queue.popleft() # 队首元素出队
	# print(url)
	visited |= {url} # 标记为已访问

	print('已经抓取: ' + str(count) + '   正在抓取 <---  ' + url)
	count += 1

	# 返回响应信息
	url_response = browser_like.return_response(url)
	if 'html' not in url_response.getheader('Content-Type'):
		continue

	# 避免程序异常中止, 用try..catch处理异常
	try:
		# 将返回的response转为字符串
		data = url_response.read().decode('utf-8')
	except:
		continue

	# 存储页面
	# 避免程序异常中止, 用try..catch处理异常
	try:
		# 将返回的response转为字符串
		file_ope.file_ope.file_save(data)
	except:
		continue

	# 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
	link_regex = re.compile('href="(http://movie\.douban\.com/subject/(?!\d+/cinema)(?!\d+/mupload)(?!\d+/wishes)(.+?))"')

	# # 创建url黑名单,符合黑名单的url不进行访问
	# url_blank_list = set()
	# blank_url = re.compile('')

	for link, value in link_regex.findall(data):
		# if 'http' in x and x not in visited:
		if link not in visited:
			queue.append(link)
			print('加入队列 --->  ' + link)

