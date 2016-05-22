import re
from functools import wraps

import requests
import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from model import *
from pytz import *


def get_movie_info(url_string, data):
    def get_info_single(tag_name, attrs=None, data=None):
        soup_local = soup
        if data:
            soup_local = BeautifulSoup(data, 'html.parser')
        r = soup_local.find_all(tag_name, attrs)
        if r:
            s = list()
            for i in r:
                s.append(i.text)
            return s
        return None

    # 创建存储影片信息的dict
    info = {
        'index': None,
        'name': None,
        'score': None,
        'score_history': defaultdict(str),
        'release_date': defaultdict(str),
        'release_year': None,
        'producing_countries': None,
        'starring': None,
        'director': None,
        'update_date': None,
        'screenwriter': None
    }

    utc_time = utc.localize(datetime.datetime.utcnow())
    utc_string = datetime.datetime.strftime(utc_time, '%Y-%m-%d:%H-%M-%S-%f')

    soup = BeautifulSoup(data, 'html.parser')

    # 如果不是电影页面，返回null
    result = soup.find_all('span', {'property': 'v:itemreviewed'})
    if not result:
        return info

    # 获取影片index
    index_regex = re.compile('.+/subject/(\d+).*')
    info['index'] = index_regex.findall(url_string)[0]

    # 抓取电影名称
    info['name'] = get_info_single('span', {'property': 'v:itemreviewed'})[0]

    # 抓取电影分数
    score = get_info_single('strong', {'property': 'v:average'})
    if score and score[0] != '':
        info['score'] = float(score[0])
        info['score_history'][utc_string] = score
    else:
        info['score_history'] = None

    # 抓取上映日期
    date_list = get_info_single('span', {'property': 'v:initialReleaseDate'})
    if date_list:
        for e in date_list:
            e = str(e[:-1])
            date = e.split('(')[0]
            try:
                country = e.split('(')[1]
            except IndexError:
                country = ""
            info['release_date'][country] = date
    else:
        info['release_date'] = None

    # 抓取电影年份
    result = soup.find('span', {'class': 'year'})
    if result and result.text != '(？)' :
        i = result.text[1:-1]
        info['release_year'] = i

    # 抓取制片国家/地区
    link_regex = re.compile('制片国家/地区:</span>\s*(.+?)\s*<br')
    result = link_regex.findall(data)
    if result:
        tmp_data = link_regex.findall(data)[0]
        r_list = tmp_data.split('/')
        s = set()
        for i in r_list:
            i = i.strip()
            s.add(i)
        info['producing_countries'] = s

    # 抓取主演
    info['starring'] = get_info_single('a', {'rel': 'v:starring'})

    # 抓取导演
    info['director'] = get_info_single('a', {'rel': 'v:directedBy'})

    # 抓取编剧
    link_regex = re.compile('(编剧</span>(.|/s)+?</span>)')
    result = link_regex.findall(data)
    if result:
        tmp_data = result[0][0]
        info['screenwriter'] = get_info_single('a', data=tmp_data)

    # 更新抓取日期
    info['update_date'] = utc_time

    return info


def store_movie(url):
    request = requests.get(url)
    data = request.text
    info = get_movie_info(url, data)
    print(info)
    movie = Movie(**info)
    if movie:
        movie.update()


# 测试get_movie_info
connect_mongodb()
store_movie("https://movie.douban.com/subject/4009950/")
