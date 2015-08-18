import re
from collections import deque

# 访问过的集合visited
visited = set()

def add_url(url)