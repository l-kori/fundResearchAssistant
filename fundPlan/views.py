import logging
from os import access
import traceback

from django.db.models import Avg
from django.http import JsonResponse
from fundPlan.models import fundList, fundData
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

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
# 添加自选股数据
def addFundListt(request):
    with open("ss.txt", "r") as f:  # 打开文件
        text = f.read()
    texts = re.findall("<a href=\"/fundinfo/(.*?).html",text)
    for k in texts:
        req = requests.get("http://121.5.252.114:8000/addfundlist?account=lxd&fundcode="+str(k)+"&isbuy=1&buytime=2021-07-15")
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

    try:
        funddata = fundList()
        funddata.fundcode = fund_code
        funddata.account = account
        funddata.isbuy = isbuy
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
    list_text = list(fundData.objects.values("fundcode").distinct())
    if len(list_text) == 0:
        logging.error(traceback.format_exc())
        logging.error("基金列表没有数据")
        return JsonResponse({"code": -6, "data": "同步失败"})
    try:
        for i in range(0,len(list_text)):
            fundcode = str(list_text[i].values())[14:-3]
            getHistoricalData(fundcode)
            logging.info(fundcode+"数据同步完成")
            logging.info("剩余未同步的数据"+len(list_text)-i)
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
        isoperation = isoperationfund(fund_list[i].account,fund_list[i].fundcode,json_text['gszzl'],0)
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

