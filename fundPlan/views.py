from django.http import JsonResponse
from fundPlan.models import fundData,fundList
from tool.historicalData import getHistoricalData
import json
import requests

# 添加自选股数据
def addFundList(request):
    fundcode = request.GET.get("fundcode")
    account = request.GET.get("account")
    text = requests.get("http://fundgz.1234567.com.cn/js/" + str(fundcode) + ".js?rt=1463558676006").text[8:-2]
    print(text)
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

    try:
        text = getHistoricalData(fundcode)
    except:
        return JsonResponse(text)
    return JsonResponse({"code": 0, "data": "成功"})

# 同步所有基金历史数据
def synchronousData(request):
    list_text = list(fundData.objects.values("fundcode").distinct())
    if len(list_text) == 0:
        return JsonResponse({"code": -5, "data": "失败"})
    text= {}

    for i in range(0,len(list_text)):
        fundcode = str(list_text[i].values())[14:-3]
        text = getHistoricalData(fundcode)
    return JsonResponse({"code": 0, "data": text})