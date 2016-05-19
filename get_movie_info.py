import re
import requests
import datetime
from bs4 import BeautifulSoup
from model import *
from pytz import *


def get_movie_info(url_string, data):
    def get_info_single(tag_name, attrs):
        r = soup.find_all(tag_name, attrs)
        s = list()
        for i in r:
            s.append(i.text)
        return s

    # 创建存储影片信息的dict
    info = {
        'index': None,
        'name': None,
        'score': None,
        'score_history': list(),
        'release_date': list(),
        'release_year': None,
        'producing_countries': None,
        'starring': None,
        'director': None,
        'update_date': None
    }

    utc_time = utc.localize(datetime.datetime.utcnow())
    utc_string = datetime.datetime.strftime(utc_time, '%Y-%m-%d:%H-%M-%S-%f')

    soup = BeautifulSoup(data, 'html.parser')

    # 如果不是电影页面，返回null
    r = soup.find_all('span', {'property': 'v:itemreviewed'})
    if len(r) is 0:
        return info

    # 获取影片index
    index_regex = re.compile('.+/subject/(\d+).*')
    info['index'] = index_regex.findall(url_string)[0]
    soup = BeautifulSoup(data, 'html.parser')

    # 抓取电影名称
    info['name'] = get_info_single('span', {'property': 'v:itemreviewed'})[0]

    # 抓取电影分数
    try:
        score = get_info_single('strong', {'property': 'v:average'})[0]
        info['score'] = float(score)
        info['score_history'].append({utc_string: score})
    except Exception:
        pass
    # 抓取上映日期
    date_list = get_info_single('span', {'property': 'v:initialReleaseDate'})
    for e in date_list:
        e = str(e[:-1])
        date = e.split('(')[0]
        try:
            country = e.split('(')[1]
        except Exception:
            country = None
        info['release_date'].append({country: date})

    # 抓取电影年份
    r = soup.find('span', {'class': 'year'})
    if r is not None:
        i = r.text[1:-1]
        info['release_year'] = i
    else:
        info['release_year'] = 0

    # 抓取制片国家/地区
    link_regex = re.compile('制片国家\/地区:<\/span>\s*(.+?)\s*<br')
    r = link_regex.findall(data)[0]
    r_list = r.split('/')
    s = set()
    for i in r_list:
        i = i.strip()
        s.add(i)
    info['producing_countries'] = s

    # 抓取主演
    info['starring'] = get_info_single('a', {'rel': 'v:starring'})

    # 抓取导演
    info['director'] = get_info_single('a', {'rel': 'v:directedBy'})

    # 更新抓取日期
    info['update_date'] = utc_time

    # print(info)
    return info


def store_movie(url):
    request = requests.get(url)
    data = request.text
    info = get_movie_info(url, data)
    print(info)
    movie = Movie(**info)
    if movie:
        movie.update()