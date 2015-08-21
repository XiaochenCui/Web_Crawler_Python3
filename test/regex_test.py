import re
import sys
import requests
# from my_package import browser_like
from bs4 import BeautifulSoup

url = 'http://movie.douban.com/subject/1304141/'
request = requests.get(url)
data = request.text
soup = BeautifulSoup(data, 'html.parser')

# 抓取电影分数
r = soup.find('strong', {'property': 'v:average'})
print('1',r.text)

# 抓取电影名称
r = soup.find('span', {'property': 'v:itemreviewed'})
print('2',r.text)

# 抓取电影年份
r = soup.find('span', {'class': 'year'})
print('3',r.text[1:-1])

# 抓取主演
r = soup.find_all('a', {'rel': 'v:starring'})
for i in r:
	print('4',i.text)

# 抓取上映日期
r = soup.find_all('span', {'property': 'v:initialReleaseDate'})
for i in r:
	print('5',i.text)

# 抓取制片国家/地区
link_regex = re.compile('制片国家\/地区:<\/span>\s*(.+?)\s*<br')
r = link_regex.findall(data)[0]
r_list = r.split('/')
for i in r_list:
	i = i.strip()
	print('6',i)

# 抓取导演
r = soup.find_all('a', {'rel': 'v:directedBy'})
for i in r:
	print('7',i.text)