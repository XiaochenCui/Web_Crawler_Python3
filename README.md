# Web_Crawler_Python3
用python3制作的网络爬虫（爬取 [豆瓣电影](https://movie.douban.com/) 的电影信息）

## 运行环境:

python 3.3+

## 使用说明:

1. 安装 [Mongodb](https://docs.mongodb.com/manual/installation/)

2. 安装库

    ```bash
    $ pip install -r requirements.txt
    ```

3. 运行daemon.py:

    ```bash
    $ python daemon.py start
    ```

## 其他:

1. 结束程序:

    ```bash
    $ python daemon.py stop
    ```

2. 查看运行日志:

    ```bash
    $ tail -f /tmp/daemon.log
    ```

3. 查看进程pid:

    ```bash
    $ tail -f /tmp/daemon.pid
    ```
    
4. 结束程序，删除数据库中所有数据及日志文件:

    ```bash
    $ python daemon.py clean
    ```

## 更新日志

### V 1.1
-bug修复
-发生异常退出时将内存中的url存入数据库

### V 1.0
-数据库更换为mongodb  
-异常处理更完善  
-内存占用优化    
-后台运行

### V 0.1 alpha
-urllib更换为第三方库responses  
-加入了http分析器BeautifulSoup的支持  
-数据被存到mysql  

### V 0.0 alpha
-可以下载电影页面并保存到data文件夹  