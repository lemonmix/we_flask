#coding=utf-8
from flask import Flask,request,render_template
from time import time
import xml.etree.ElementTree as et
import hashlib
import requests,json
import pymysql
import text_templet

app = Flask(__name__)

@app.route("/")
def index():
    db = pymysql.connect(user='root', password='root', database='data', port=3306, charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM github_info"
    cursor.execute(sql)
    info_lists = cursor.fetchall()
    info_res = list(info_lists)
    info_list = []
    for line in info_res:
        link = {}
        name = ['url', 'title', 'stars',
                'collect_time', 'source_url','description']
        i = 0
        for one in line:
            link[name[i]] = one
            i = i+1
        info_list.append(link)
    db.close()
    return render_template('web.html', info_list =info_list)

@app.route("/wx",methods=['GET','POST'])
def wechat():
    if request.method == 'GET':
       token = 'coder'
       data = request.args
       print(data)
       signature = data.get('signature','')
       timestamp = data.get('timestamp','')
       nonce = data.get('nonce','')
	   echostr = data.get('echostr','')
       list = [token,timestamp,nonce]
       list.sort()
       s = list[0]+list[1]+list[2]
       hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
       if hascode == signature:
          return echostr
       else:
          return ""

    if request.method == 'POST':
       xmldata = request.data
       xml_rec = et.fromstring(xmldata)

       ToUserName = xml_rec.find('ToUserName').text
       fromUser = xml_rec.find('FromUserName').text
       MsgType = xml_rec.find('MsgType').text
       Content = xml_rec.find('Content').text
       MsgId = xml_rec.find('MsgId').text
       if Content == 'info':
          Content = 'http://154.8.175.97/'
		  return text_templet.reply_templet(MsgType) % (fromUser, ToUserName, str(int(time())), Content)
       return text_templet.reply_templet(MsgType)%(fromUser,ToUserName,str(int(time())),reply(fromUser,Content))

def reply(openid,msg):
    #key后填入自己的图灵机器人apikey
    data = {"key":"*****","info":msg,"userid":openid}
    r = requests.post('http://openapi.tuling123.com/openapi/api',data)
    text = json.loads(r.text)
    return text['text']

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)

