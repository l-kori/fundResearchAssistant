import requests
import json
from django.http import JsonResponse
from fundPlan.models import fundData,fundList
from tool.historicalData import getHistoricalData
import time
import requests
import re

#定时任务，每5分钟抓取一次数据
def getFundData(request):
    id = request.GET.get("account")
    try:
        list = fundList.objects.filter(account=id)
    except:
        return JsonResponse({"code": -3, "data": "失败"})
    for i in range(0,len(list)):
        fundcode = list[i].fundcode
        print(fundcode)
        # 查询数据库是否有这只基金数据
        today = time.strftime("%Y-%m-%d", time.localtime())
        count = fundData.objects.filter(fundcode=fundcode,gztime=str(today)).count()
        if count > 0:
            continue
        text = requests.get("http://fundgz.1234567.com.cn/js/" + fundcode + ".js?rt=1463558676006").text[8:-2]
        try:
            json_text = json.loads(text)
        except:
            return JsonResponse({"code": -2, "data": "失败"})
        fund_name = json_text['name']
        fund_code = json_text['fundcode']
        # 实际净值
        fund_sjjz = float(json_text['dwjz'])
        # 净值日期
        fund_jzrq = json_text['jzrq']
        # 最新净值
        fund_gsz = float(json_text['gsz'])
        # 最新涨幅
        fund_gszzl = float(json_text['gszzl'])
        # 最新净值时间
        fund_gztime = json_text['gztime']

    return JsonResponse({"code": 200, "data": "完成"})

def addFundList(request):
    fundcode = request.GET.get("fundcode")
    account = request.GET.get("account")
    text = requests.get("http://fundgz.1234567.com.cn/js/" + str(fundcode) + ".js?rt=1463558676006").text[8:-2]
    try:
        json_text = json.loads(text)
    except:
        return JsonResponse({"code": -2, "data": "失败"})
    fund_code = json_text['fundcode']
    try:
        funddata = fundList()
        funddata.fundcode = fund_code
        funddata.account = account
        funddata.save()
    except:
        return JsonResponse({"code": -1, "data": "失败"})
    return JsonResponse({"code": 0, "data": "成功"})


def fundlist(request):
    id = request.GET.get("account")
    list1 = fundList.objects.all().filter(account=id)
    data = []
    for i in range(0,len(list1)):
        fundcode = list1[i].fundcode
        today = time.strftime("%Y-%m-%d", time.localtime())
        res = list(fundData.objects.filter(fundcode=fundcode, gztime=str(today)).values())
        data.append(res)
    return JsonResponse({"code": 0, "data": data})


def historicalData(request):
    fundCode = request.GET.get("fundCode")
    text = getHistoricalData(fundCode)
    return JsonResponse(text)


def synchronousData(request):
    id = request.GET.get("account")
    try:
        list = fundList.objects.filter(account=id)
    except:
        return JsonResponse({"code": -3, "data": "失败"})
    for i in range(0, len(list)):
        fundcode = list[i].fundcode
        text = getHistoricalData(fundcode)
        return JsonResponse(text)