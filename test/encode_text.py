import codecs
f = codecs.open('test.txt', 'w', 'utf-8')
f.write('中文')
f.close()