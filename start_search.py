import re
import requests
import time
# import sys
# print(sys.path)
from collections import deque
# from bs4 import BeautifulSoup

import mysql_ope
import get_movie_info
# from my_package import file_ope

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
while queue and count <= 20:
	time.sleep(1)

	url = queue.popleft() # 队首元素出队
	visited |= {url} # 标记为已访问

	print('已经抓取: ' + str(count) + '   正在抓取 <---  ' + url)
	count += 1

	# 返回url对应的页面内容
	# 用try...处理异常
	try:
		request = requests.get(url)
		data = request.text
	except Exception:
		continue

	# 存储页面
	# file_ope.file_ope.file_save(data)

	# 提取影片信息
	info = get_movie_info.get_info(data)
	if(len(info) is not 0):
		print(info)
		mysql_ope.info_save(info)
		pass

	# 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
	link_regex = re.compile('href="(http://movie\.douban\.com/subject/\d+/).+?"')

	for link in link_regex.findall(data):
		if link not in visited and link not in queue:
			queue.append(link)
			print('加入队列 --->  ' + link)

