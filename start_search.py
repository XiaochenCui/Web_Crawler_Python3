import re
import traceback

import requests
import time
from collections import deque

from get_movie_info import get_movie_info
from model import *
from tool.print_tool import errprint


class Search(object):
    def __init__(self):
        self.count = 0
        # 待访问的集合queue
        self.queue = deque()

    def main(self):
        # 连接数据库
        connect_mongodb()

        # 入口页面
        url_start = "http://movie.douban.com/"
        Url.add_url(url_start)

        while Url.objects(access=False):
            self.queue = list(Url.objects(access=False)[:200])
            print("从数据库中获取---{}---个url".format(len(self.queue)))

            # 遍历queue
            self.traversal_queue(self.queue)

    def traversal_queue(self, queue):
        for url in queue:
            time.sleep(1)

            print('已经抓取: ' + str(self.count) + '   正在抓取 <---  ' + url.url)
            self.count += 1

            # 返回url对应的页面内容
            # 用try...处理异常
            try:
                request = requests.get(url.url, timeout=5)
                data = request.text
            except Exception:
                BadUrl.add(url.url)
                errprint("""----------------------------------------------------"
                Exception occur when get web data:""")
                traceback.print_exc()
                errprint("bad url: {}".format(url.url))
                continue

            # 提取影片信息
            # 用try...处理异常
            try:
                info = get_movie_info(url.url, data)
                if info['index']:
                    print('电影---{}---的信息:\n{}'.format(info['name'], info))
                    movie = Movie(**info)
                    if movie:
                        movie.update()
            except  Exception:
                BadUrl.add(url.url)
                errprint("""----------------------------------------------------"
                    Exception occur when get web data:""")
                traceback.print_exc()
                errprint("bad url: {}".format(url.url))
                continue

            # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
            link_regex = re.compile('href="(https?://movie\.douban\.com/subject/\d+).+?"')

            for link in set(link_regex.findall(data)):
                if not Url.objects(url=link) and not BadUrl.objects(url=link):
                    print('加入数据库 --->  [{position}]      {url}'.format(position=Url.objects().count, url=link))
                    Url.add_url(link)

            # 将url标记为已访问
            url.update(True)
