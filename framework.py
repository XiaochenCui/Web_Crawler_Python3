set url_set_haveBeenVisited
queue url_queue_waitForVisited

queue #待访问队列

set #访问过的集合

url_start = "http://movie.douban.com/"
url_queue_waitForVisited.push(url_start)

while (url_queue_waitForVisited.size() > 0):
		#拿出队列中第一个url
		url_current = url_queue_waitForVisited.get()
		#存储这个url代表的网页
		store(url_current)
		for url_next in extract_url(url_current):
			if url_next not in url_set_haveBeenVisited:
				url_set_haveBeenVisited.put(url_next)
				url_queue_waitForVisited.put(url_next)
