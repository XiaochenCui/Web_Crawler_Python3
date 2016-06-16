from time import sleep

import cssutils
import requests
from bs4 import BeautifulSoup
import datetime
from pytz import *

from model import Proxy, connect_mongodb


def search_proxy():
    url = "http://cn-proxy.com/"
    data = ""
    # while not data or data == "":
    #     try:
    #         data = requests.get(url).text
    #     except Exception:
    #         sleep(2)
    #         continue

    with open('/home/chenxiao/document/data', 'rt') as f:
        data = f.read()

    soup = BeautifulSoup(data, 'html.parser')
    tbody = soup.findAll('tbody')[1]
    tr_list = tbody.findAll('tr')
    for tr in tr_list:
        td_list = tr.findAll('td')

        proxy = Proxy()

        speed = get_speed(td_list[3])
        if speed < 70:
            continue

        proxy.speed = speed
        proxy.url = td_list[0].text + ":" + td_list[1].text
        proxy.position = td_list[2].text
        time_string = td_list[4].text
        time = datetime.datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S')
        time = timezone('Asia/Shanghai').localize(time)
        utc_time = time.astimezone(utc)
        proxy.last_check = utc_time

        if not Proxy.objects(url=proxy.url):
            print("加入代理服务器:   {}".format(proxy.url))
            proxy.save()


def get_speed(td):
    speed_style = td.find('strong').attrs['style']
    speed_style_width = cssutils.parseStyle(speed_style).width
    speed = int(speed_style_width[:-1])
    return speed

# connect_mongodb()
# search_proxy()
#
# # 如果需要使用代理，你可以通过为任意请求方法提供 proxies 参数来配置单个请求:
#
# import requests
#
# proxies = {
#   "http": "http://10.10.1.10:3128",
#   "https": "http://10.10.1.10:1080",
# }
#
# requests.get("http://example.org", proxies=proxies)

