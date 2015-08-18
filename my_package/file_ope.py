file_index = 0
class file_ope(object):
	file_index = 0

	def file_save(data):
		file_ope.file_index += 1
		path_save = r'C:\Users\Administrator\Documents\GitHub\Web_Crawler_Python3\data\web_date_'+str(file_ope.file_index)+'.out'
		file_obj = open(path_save, 'w')
		# file_obj.write('/xEF/xBB/xBF')
		file_obj.write(data)
		file_obj.close()
		print('save_success:'+path_save)
		return 1