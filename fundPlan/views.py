import requests
import json
from django.http import JsonResponse
from fundPlan.models import fundData,fundList
import time
#定时任务，每5分钟抓取一次数据库里的所有数据并写入数据库
def getFundData(request):
    id = request.GET.get("account")
    try:
        list = fundList.objects.filter(account=id)
    except:
        return JsonResponse({"code": -3, "data": "失败"})
    for i in range(0,len(list)):
        fundcode = list[i].fundcode
        # 查询数据库是否有这只基金数据
        today = time.strftime("%Y-%m-%d", time.localtime())
        print(today)
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
        try:
            funddata = fundData()
            funddata.fundcode = fund_code
            funddata.name = fund_name
            funddata.sjjz = fund_sjjz
            funddata.jzrq = fund_jzrq
            funddata.zxjz = fund_gsz
            funddata.zxzf = fund_gszzl
            funddata.gztime = today
            funddata.save()
            # cur_date = datetime.timedelta.now().date()
            # import datetime
            # # 一天前的日期
            # yester_day = str(cur_date - datetime.timedelta(days=1))

        except:
            return JsonResponse({"code": -1, "data": "失败"})

    return JsonResponse({"code": 200, "data": "完成"})

def addFundList(request):
    fundCode = request.GET.get("fundCode")
    text = requests.get("http://fundgz.1234567.com.cn/js/" + fundCode + ".js?rt=1463558676006").text[8:-2]
    try:
        json_text = json.loads(text)
    except:
        return JsonResponse({"code": -2, "data": "失败"})
    fund_code = json_text['fundcode']
    try:
        funddata = fundList()
        funddata.fundcode = fund_code
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