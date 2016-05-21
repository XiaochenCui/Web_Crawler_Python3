import requests

from my_package import get_movie_info

url = 'http://movie.douban.com/subject/1304141/'
request = requests.get(url)
data = request.text

print(get_movie_info.get_info(data))