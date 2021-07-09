import logging
import traceback

from django.http import JsonResponse
from fundPlan.models import fundList, fundData
from tool.historicalData import getHistoricalData
import json
import requests
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)
# 添加自选股数据
def addFundList(request):
    fundcode = request.GET.get("fundcode")
    account = request.GET.get("account")
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
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        logging.error("同步失败")
        return JsonResponse({"code": -6, "data": "同步失败"})
    return JsonResponse({"code": 0, "data": "成功"})