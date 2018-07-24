import multiprocessing
from multiprocessing import Pool as ThreadPool
import string, re, ftplib, time
import requests, pymysql


class get_from_github(object):
    def __init__(self):
        self.time = time.strftime("%m_%d_%H_%M_%S", time.localtime())
        self.ID = 1

    def get_url_from_mysql(self):
        db = pymysql.connect(user='root', password='root', database='data', port=3306, charset='utf8')
        cursor = db.cursor()
        sql = "SELECT DISTINCT github FROM github_adr"
        cursor.execute(sql)
        url_lists = cursor.fetchall()
        url_res = list(url_lists)
        url_list = []
		for line in url_res:
            for i in line:
                if (i != ''):
                    url_list.append(i)
        db.close()
        return url_list

    def get_surl(self, url):
        db = pymysql.connect(user='root', password='root', database='data', port=3306, charset='utf8')
        cursor = db.cursor()
        sql = "SELECT url FROM github_adr WHERE github = %s"
        # cursor.executemany(sql,data)
        cursor.execute(sql, url)
        surl = cursor.fetchall()
        surl_temp = list(surl)
        surl_res = []
        for line in surl_temp:
            for i in line:
                if (i != ''):
                    surl_res.append(i)
        db.close()
		print(surl_res)
        return surl_res[0]

    def get_time(self, url):
        db = pymysql.connect(user='root', password='root', database='data', port=3306, charset='utf8')
        cursor = db.cursor()
        sql = "SELECT collect_time FROM github_adr WHERE github = %s"
        # cursor.executemany(sql,data)
        cursor.execute(sql, url)
        collect_time = cursor.fetchall()
        collect_time_temp = list(collect_time)
        collect_time_res = []
        for line in collect_time_temp:
            for i in line:
                if (i != ''):
                    collect_time_res.append(i)
        db.close()
        print(collect_time_res)
        return collect_time_res[0]
		
	def start_request(self, url):
        try:
            self.ID += 1
            data = requests.get(url)
            data.encoding = 'utf-8'
            # print(data.text)
            s = data.text
            if s != 'Not Found':
                print(url)
                title = re.findall('https://github.com/.*/(.*)', url)
                if title != []:
                    title = title[0]
                else:
                    title = ''
                description = re.findall('<title>.*:\s(.*)</title>', s)
                if description != []:
                    description = description[0]
                else:
                    description = ''
                author = re.findall('https://github.com/(.*)/', url)
                if author != []:
                    author = author[0]
                else:
				    author = ''
                stars = re.findall('aria-label="(\d*) users starred this repository"', s)
                if stars != []:
                    stars = stars[0]
                else:
                    stars = ''

                collect_time = self.get_time(url)
                source_url = self.get_surl(url) #注意调用类内函数需要加上类名或self
                print(title)
                print(description)
                print(stars)
                print(collect_time)
                print(url)
                print(source_url)
                return (url, title,description,stars,collect_time,source_url)
            return None
        except TimeoutError:
            return None
        except ConnectionError:
		    return None
    def insert_db(self, data):
        db = pymysql.connect(user='root', password='root', database='data', port=3306, charset='utf8')
        cursor = db.cursor()
        sql = "INSERT INTO github_info(url, title,description,stars,collect_time,source_url) " \
              "VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.executemany(sql, data)
        db.commit()
		
if __name__ == "__main__":
    start_time = time.time()
    pool = ThreadPool(multiprocessing.cpu_count() * 2)
    wtf = get_from_github()
    github_lists = wtf.get_url_from_mysql()
    print(github_lists)
    print(len(github_lists))
    results = list(pool.map(wtf.start_request, github_lists))
    pool.close()
    pool.join()
    print(results)
    print(len(results))
    result = []
    for i in results:
        if i != None:
            result.append(i)
    print(result)
    end_time = time.time()
    cost = end_time - start_time  # time in second
    print('耗时为：')
    print(cost)
    wtf.insert_db(result)  # 
    print('插入数据库成功')


