import logging
from os import access
import traceback

from django.db.models import Avg
from django.http import JsonResponse
from fundPlan.models import fundList, fundData, mindata
from tool.historicalData import getHistoricalData
from tool.gainsCount import isoperationfund
from tool.sendEmail import remindWarehouse
import json
import requests
from django.db.models import Avg
import datetime
from django.forms.models import model_to_dict
from django.core import serializers
import time
import re
import threading
from tool.sp import login,qdxd,qdxd1

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
# 添加自选股数据
def addFundListt(request):
    with open("ss.txt", "r") as f:  # 打开文件
        text = f.read()
    texts = re.findall("<a href=\"/fundinfo/(.*?).html",text)
    for k in texts:
        req = requests.get("http://127.0.0.1:8000/addfundlist?account=lxd&fundcode="+str(k)+"&isbuy=1&buytime=2021-07-15")
        logging.info(req.text)
    return JsonResponse({"code": -2, "data": "失败"})

def addFundList(request):
    fundcode = request.GET.get("fundcode")
    account = request.GET.get("account")
    # 1= 买了，0=没买
    isbuy = request.GET.get("isbuy",0)

    isexit = fundList.objects.filter(account=account,fundcode=fundcode)
    if len(isexit) != 0:
        logging.info("数据已存在，无需再添加")
        return JsonResponse({"code": -2, "data": "数据已存在，无需再添加"})
    text = requests.get("http://fundgz.1234567.com.cn/js/" + str(fundcode) + ".js?rt=1463558676006").text[8:-2]
    try:
        json_text = json.loads(text)
    except Exception as e:
        logging.error("添加失败，不是json格式")
        logging.error(e)
        logging.error(traceback.format_exc())
        return JsonResponse({"code": -2, "data": "失败"})
    fund_code = json_text['fundcode']
    fund_name = json_text['name']

    try:
        funddata = fundList()
        funddata.fundcode = fund_code
        funddata.account = account
        funddata.isbuy = isbuy
        funddata.fundname = fund_name
        funddata.save()
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        logging.error(fund_code +"写入自选股表失败")
        return JsonResponse({"code": -1, "data": "失败"})

    try:
        text = getHistoricalData(fundcode)
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        logging.error(fund_code +"写入数据库失败")
        return JsonResponse({"code": -1, "data": "失败"})
    return JsonResponse({"code": 0, "data": "成功"})


def removeFundList(request):
    fundcode = request.GET.get("fundcode")
    account = request.GET.get("account")
    try:
        fundList.objects.filter(account=account,fundcode=fundcode).delete()
        logging.info(account +fundcode + "删除自选股")
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        logging.error(account +fundcode + "删除自选股失败")
        return JsonResponse({"code": -1, "data": "失败"})
    return JsonResponse({"code": 0, "data": "成功"})


# 同步所有基金历史数据
def synchronousData(request):
    
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday 
    date = str(yesterday)+' 00:00:00.000000'
    logging.info("开始同步"+date+"数据")
    list_text = fundList.objects.values('fundcode').distinct()
    # print(list_text)
    try:
        for i in range(len(list_text)) :
            fundcode = str(list_text[i].values())[14:-3]
            res = fundData.objects.filter(fundcode = fundcode,jzrq=date)
            if len(res) == 0:
                t = threading.Thread(target=getHistoricalData,args=(fundcode,))
                t.start()
            else:
                logging.info(fundcode + "----" + date+"数据存在，无需同步")
                re_text = "成功"
            logging.info("剩余未同步的数据"+str(len(list_text)-i))
            print("剩余未同步的数据"+str(len(list_text)-i))
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        logging.error("同步失败")
        return JsonResponse({"code": -6, "data": "同步失败"})
    return JsonResponse({"code": 0, "data": "成功"})



# 用户实时数据
def userLiveData(request):
    account = request.GET.get("account")
    list_text = fundList.objects.filter(account=account)
    if len(list_text) == 0:
        logging.info(account+"用户自选股数据为空")
        return JsonResponse({"code": -7, "data": "用户自选股数据为空"})
    fund_list = []
    for i in list_text:
        text = requests.get("http://fundgz.1234567.com.cn/js/" + str(i.fundcode) + ".js?rt=1463558676006").text[8:-2]
        try:
            json_text = json.loads(text)
            json_text['isbuy'] = str(i.isbuy)
            print(json_text)
            fund_list.append(json_text)
        except Exception as e:
            logging.error("用户实时数据查询失败")
            logging.error(e)
            logging.error(traceback.format_exc())
            return JsonResponse({"code": -2, "data": "失败"})
    return JsonResponse({"code": 0, "data": fund_list})


# 定时检查数据，是否需要加仓
def fundTips(request):
    # 查询数据，已购买的数据进行检查
    fund_list = fundList.objects.filter(isbuy='1')
    warehouseList = []
    for i in range(0,len(fund_list)):
        # 查询基金今日涨幅
        text = requests.get("http://fundgz.1234567.com.cn/js/" + fund_list[i].fundcode + ".js?rt=1463558676006").text[8:-2]
        try:
            json_text = json.loads(text)
        except Exception as e:
            logging.error("用户实时数据查询失败")
            logging.error(e)
            logging.error(traceback.format_exc())
            return JsonResponse({"code": -2, "data": "失败"})
        isoperation = isoperationfund(fund_list[i].account,fund_list[i].fundcode,float(json_text['gszzl']),0)
        if isoperation == 1:
            # 发送邮件
            res = remindWarehouse(fund_list[i].fundcode,fund_list[i].account,1)
            if res:
                logging.info(fund_list[i].account+"----"+fund_list[i].fundcode+"调仓邮件已发送")
        if isoperation == 0:
            logging.info(fund_list[i].account+"--"+fund_list[i].fundcode+"--未达到持仓操作要求，不建议操作")
            
        if isoperation == 2:
            res = remindWarehouse(fund_list[i].fundcode,fund_list[i].account,2)
            if res:
                logging.info(fund_list[i].account+"----"+fund_list[i].fundcode+"调仓邮件已发送")
            
        return JsonResponse({"code": 0, "data": "完成"})



def fundProfit(request):
    # 查询列表里所有已经买了的基金则进行当日交易计算
    fund_result = fundList.objects.filter(isbuy=1)
    for i in  range(0,len(fund_result)):
        # 查询这只基金的当天实际涨幅
        fund_zf = fundData.objects.get(fundcode=fund_result[i].fundcode,jzrq='2021-07-15')
        profit = fundList.objects.get(fundcode=fund_result[i].fundcode,account=fund_result[i].account)
        profit.fundPosition += fund_result[i].fundPosition*fund_zf.jrzf/100
        if fund_result[i].fundProfitRate ==0:
            profit.fundProfitRate += fund_zf.jrzf
        profit.fundProfitRate += fund_zf.jrzf*fund_result[i].fundProfitRate/10
        profit.fundProfitMoney += fund_zf.jrzf*fund_result[i].fundPosition/100
        profit.save()
       
    return JsonResponse({"code": 0, "data": "成功"})

def queryFundToCode(request):
    fundcode = request.GET.get("fundcode")
    try:
        req = fundList.objects.filter(fundcode__contains=fundcode,account='lxd')[:6]
        if len(req)==0:
            logging.info("没有这个基金")
            return JsonResponse({"code": -11, "data": "失败"})
        infos = []
        for i in req:
            infos.append(model_to_dict(i))  # 对象转为字典
            res = {
                "code": 0,
                "data": {
                    "infos": infos,
                    "total": len(infos)
                }
            }
    except Exception as e:
        logging.error("查询基金数据失败")
        logging.error(e)
        logging.error(traceback.format_exc())
        return JsonResponse({"code": -1, "data": "失败"})
    return JsonResponse(res)

# 爬取分时数据，写入数据库
def crawlMinData(request):
    res = fundList.objects.exclude(account='lxd')
    for i in res:
        text = requests.get("http://fundgz.1234567.com.cn/js/" + i.fundcode + ".js?rt=1463558676006").text[8:-2]
        json_text = json.loads(text)

        min = mindata()
        min.fundcode = i.fundcode
        min.datatime = json_text['gztime']
        min.zf = json_text['gszzl']
        min.save()
        logging.info(i.fundcode+"写入成功")

    return JsonResponse({"code": 0, "data": "完成"})

# 分时数据
def minData(request):
    fundcode = request.GET.get("fundcode")
    req = mindata.objects.filter(fundcode=fundcode)
    res = {}
    infos = []
    for i in req:
        infos.append(model_to_dict(i))  # 对象转为字典
        res = {
            "code": 0,
            "data": {
                "infos": infos,
                "total": len(infos)
            }
        }
    return JsonResponse({"code": 0, "data": res})


def yumaoqiulogs(request):
    text = []
    with open("ymqgo.txt","r",encoding='utf8') as f:
        for line in f.readlines():
            line = line.split('\n')
            print(line)
            text.append(line)
    text.reverse()
    return JsonResponse({"code": 0, "data": text})

def yumaoqiugo(request):
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
        import datetime
        
        count = 0
        while 1:
            count +=1
            if count == 5:
                import os
                path = 'ymqgo.txt'  # 文件路径
                if os.path.exists(path):  # 如果文件存在
                    # 删除文件，可使用以下两种方法。
                    os.remove(path)  
                    #os.unlink(path)
                else:
                    print('no such file')  # 则返回文件不存在
                break
            ss = time.strftime("%H:%M:%S", time.localtime())
            nowdate = datetime.datetime.now()
            stime = (nowdate + datetime.timedelta(days=+8)).strftime("%Y-%m-%d")
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
        return JsonResponse({"code": 1, "data": "完成"})
    except :
        return JsonResponse({"code": 1, "data": "失败"})

def yumaoqiuview(request):
    from tool.sp import login
    res = login()
    Authorization = 'Bearer '+res
    url = "http://order.51yundong.me/v3/orders/user?pageNo=1&pageSize=30&orderStatus=3"

    payload={}
    headers = {
    'Authorization': Authorization,
    '1yd_source': 'android_user',
    '1yd_version': '3.8.6_RELEASE',
    'Host': 'order.51yundong.me',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/3.11.0'
    }

    response = requests.request("GET", url, headers=headers, data=payload).text
    res_json = json.loads(response)
    data = []
    for i in range(0,len(res_json['data']['dataList'])):
        if res_json['data']['dataList'][i]['orderField'][0]['paymentStatusMsg'] == '已支付':
            data.append([res_json['data']['dataList'][i]['fieldName'],
                res_json['data']['dataList'][i]['resourceDate'],
                res_json['data']['dataList'][i]['orderField'][0]['beginTime'],
                res_json['data']['dataList'][i]['orderField'][0]['endTime'],
                res_json['data']['dataList'][i]['cancelOrderTime']
            ])
    data.reverse()
    return JsonResponse({"code": 1, "data": data})