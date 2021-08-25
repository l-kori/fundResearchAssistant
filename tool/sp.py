import requests
import json
import time
import threading

import smtplib
from email.mime.text import MIMEText
import requests
import time

def wlog(msg):
    with open("ymqgo.txt","a",encoding='utf8') as f:
        f.write(msg+'\n')

def sendmessage(message):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=f73b7110a26939d61f41e05f3e7617affee7511324f047e8ce5b1ad00b84c4e9' #钉钉机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = message
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
         "at": {
            "isAtAll": 1                                         #如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)

    



def remindWarehouse(msg):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'  
    #163用户名
    mail_user = '15279797051'  
    #密码(部分邮箱为授权码) 
    mail_pass = 'XUBGFRAZFJDDURLL'   
    #邮件发送方邮箱地址
    sender = '15279797051@163.com'  
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['15279797051@163.com']  

    #设置email信息
    #邮件内容设置
    message = MIMEText('抢到了','plain','utf-8')
    #邮件主题       
    message['Subject'] = msg 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
        return True
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
        return False



def login():
    import requests

    url = "http://auth.51yundong.me/v3/oauth/token"

    payload='client_id=68fcd83dc5cf11e6bfe20242ac11001c&client_secret=88e92e35c5cf11e6bfe20242ac11001c&grant_type=password&username=15279797051&password=kori1998'
    headers = {
    '1yd_source': 'android_user',
    '1yd_version': '3.8.6_RELEASE',
    'Host': 'auth.51yundong.me',
    'User-Agent': 'okhttp/3.11.0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'cat=15c8b185e3933adc8c6d8757e9623b5a'
    }

    response = requests.request("POST", url, headers=headers, data=payload).text

    res_json = json.loads(response)
    return res_json['data']['access_token']


def pyxd():
    try:
        import os
        path = "ymqgo.txt"  # 文件路径
        if os.path.exists(path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            os.remove(path)  
            #os.unlink(path)
        else:
            print('no such file')  # 则返回文件不存在
        # 登录
        res = login()
        Authorization = 'Bearer '+res
        print(Authorization)
        wlog("登录成功")
        import datetime
        nowdate = datetime.datetime.now()
        stime = (nowdate + datetime.timedelta(days=+8)).strftime("%Y-%m-%d")
        print(stime)
        while 1:
            ss = time.strftime("%H:%M:%S", time.localtime())
            if ss == '00:30:00':
                wlog("结束了")
                import os
                path = 'D:\code\fundResearchAssistant\ymqgo.txt'  # 文件路径
                if os.path.exists(path):  # 如果文件存在
                    # 删除文件，可使用以下两种方法。
                    os.remove(path)  
                    #os.unlink(path)
                else:
                    print('no such file')  # 则返回文件不存在
                wlog("-------------------------------------------------------------------------")
                break
            # 找场地
            url = "http://transfer.51yundong.me/v3/resource_transfer/new/3fb03d294a564d3e9cde7b8c5c0a90b4?date="+stime+""
            payload={}
            headers = {
            'Authorization': 'Bearer ' + Authorization,
            '1yd_source': 'android_user',
            '1yd_version': '3.8.6_RELEASE',
            'Host': 'transfer.51yundong.me',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.11.0'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            s = json.loads(response.text)
            ss = s['data']
            ss.reverse()
            fieldId = ss[5]['field_id']
            fildidnub =ss[5]['field_name']

            for i in ss:
                fieldId= i['field_id']
                fildidnub= i['field_name']
                # 下单
                t = threading.Thread(target=qdxd,args=(fieldId,fildidnub,stime,Authorization))
                t.start()
                t1 = threading.Thread(target=qdxd1,args=(fieldId,fildidnub,stime,Authorization))
                t1.start()
            time.sleep(5)
    except :
        print("异常")
        
def qdxd(fieldId,fildidnub,stime,Authorization):
    url = "http://order.51yundong.me/v3/orders"

    payload = json.dumps({
    "channel": 6,
    "orderDetailField": [
        {
        "beginTime": "20:00",
        "endTime": "21:00",
        "fieldId": fieldId,
        "fieldName": fildidnub,
        "resourceDate": stime,
        "stadiumId": "969d020da8504cfa9b159498e79ff88d",
        "stadiumItemId": "3fb03d294a564d3e9cde7b8c5c0a90b4"
        }
    ],
    "orderType": 1,
    "remark": "android"
    })
    headers = {
    'Authorization': Authorization,
    '1yd_source': 'android_user',
    '1yd_version': '3.8.6_RELEASE',
    'Content-Type': 'application/json',
    'Content-Length': '523',
    'Host': 'order.51yundong.me',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.11.0'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    
        res_json = json.loads(response.text)
        if res_json['success'] != 'F':
            remindWarehouse('八点场抢到了')
            sendmessage("八点场抢到了")
            wlog("八点场抢到了")
        else:
            wlog(str(res_json))
    except :
        wlog("异常")
def qdxd1(fieldId,fildidnub,stime,Authorization):
    url = "http://order.51yundong.me/v3/orders"

    payload = json.dumps({
    "channel": 6,
    "orderDetailField": [
        {
        "beginTime": "21:00",
        "endTime": "22:00",
        "fieldId": fieldId,
        "fieldName": fildidnub,
        "resourceDate": stime,
        "stadiumId": "969d020da8504cfa9b159498e79ff88d",
        "stadiumItemId": "3fb03d294a564d3e9cde7b8c5c0a90b4"
        }
    ],
    "orderType": 1,
    "remark": "android"
    })
    headers = {
    'Authorization': Authorization,
    '1yd_source': 'android_user',
    '1yd_version': '3.8.6_RELEASE',
    'Content-Type': 'application/json',
    'Content-Length': '523',
    'Host': 'order.51yundong.me',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.11.0'
    }

    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        res_json = json.loads(response.text)
        if res_json['success'] != 'F':
            remindWarehouse('九点场抢到了')
            sendmessage("九点场抢到了")
            wlog("九点场抢到了")
        else:
            wlog(str(res_json))
    except :
        wlog("异常")
    