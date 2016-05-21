# Web_Crawler_Python3
用python3制作的网络爬虫（爬取 [豆瓣电影](https://movie.douban.com/) 的电影信息）

运行环境:

python 3.3+

使用说明:

1, 安装 [Mongodb](https://docs.mongodb.com/manual/installation/)

2, 安装库

```bash
$ pip install -r requirements.txt
```

3, 运行daemon.py:

```bash
$ python daemon.py start
```

其他:

1, 结束程序:

```bash
$ python daemon.py stop
```

2, 查看运行日志:

```bash
$ tail -f /tmp/daemon.log
```

3, 查看进程pid:

```bash
$ tail -f /tmp/daemon.pid
```

## V 1.1
-bug修复

## V 1.0
-数据库更换为mongodb  
-异常处理更完善  
-内存占用优化  
-彻底的代码重构  

##V 0.1 alpha
-urllib更换为第三方库responses  
-加入了http分析器BeautifulSoup的支持  
-数据被存到mysql  

##V 0.0 alpha
-可以下载电影页面并保存到data文件夹  