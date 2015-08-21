import pymysql.cursors
import time

# Connect to the database
# a = 7.5465465
# print(time.time())
# print(time.strftime("%Y-%m-%d", time.localtime()))

def info_save(info):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='web_data',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO movie_info (name, score, release_date, release_year, producing_countries, starring, director) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            a = cursor.execute(sql, (info['name'], info['score'], '2000.1.1', info['release_year'], str(info['producing_countries']), str(info['starring']), str(info['director'])))
            
            # print(str(info['release_date']))
    
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    
        # with connection.cursor() as cursor:
        #     # Read a single record
        #     sql = "SELECT * FROM movie_info"
        #     cursor.execute(sql)
        #     result = cursor.fetchone()
        #     print(result)
    finally:
        connection.close()

# info_save()