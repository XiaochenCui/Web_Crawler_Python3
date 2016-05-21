import re
import requests
import time
from collections import deque

from get_movie_info import get_movie_info
from model import *


class Search(object):

    def __init__(self):
        self.count = 0
        self.add_to_queue = True
        # 待访问的集合queue
        self.queue = deque()

    def main(self):
        # 连接数据库
        connect_mongodb()

        # 入口页面
        url_start = "http://movie.douban.com/"
        url = Url(url=url_start)

        self.queue.append(url)

        while self.queue or Url.objects(access=False):
            url_queue = list(Url.objects(access=False)[:200])
            print("从数据库中获取---{}---个url".format(len(url_queue)))
            self.queue.extend(url_queue)

            print("现在有---{}---个url在队列中".format(len(self.queue)))
            self.add_to_queue = True

            # 异常退出时将内存中的url存入数据库
            try:
                self.traversal_queue(self.queue)
            except Exception:
                for url in self.queue:
                    url.save()
                raise SystemExit(1)

    def traversal_queue(self, queue):
        while queue:
            time.sleep(1)

            url = queue.popleft()  # 队首元素出队

            print('已经抓取: ' + str(self.count) + '   正在抓取 <---  ' + url.url)
            self.count += 1

            # 返回url对应的页面内容
            # 用try...处理异常
            try:
                request = requests.get(url.url, timeout=5)
                data = request.text
            except Exception:
                continue

            # 提取影片信息
            info = get_movie_info(url.url, data)
            if info['index']:
                print('电影---{}---的信息:\n{}'.format(info['name'], info))
                movie = Movie(**info)
                if movie:
                    movie.update()

            # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
            link_regex = re.compile('href="(https?://movie\.douban\.com/subject/\d+).+?"')

            for link in link_regex.findall(data):
                if not Url.objects(url=link).first() and link not in queue:
                    url_new = Url(url=link)
                    if len(queue) < 200 and self.add_to_queue:
                        queue.append(url_new)
                        print('加入队列 --->  [{position}]      {url}'.format(position=len(queue), url=link))
                    else:
                        self.add_to_queue = False
                        Url.add_url(link)

            url.update(True)
