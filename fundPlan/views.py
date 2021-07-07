import requests
import json
from django.http import JsonResponse
from fundPlan.models import fundData,fundList
import time
import requests
import re

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


def historicalData(request):
    fundCode = request.GET.get("fundCode")
    today = time.strftime("%Y-%m-%d", time.localtime())
    url = "https://www.dayfund.cn/fundvalue/"+fundCode+".html?sdate=2021-04-07&edate="+str(today)+""

    payload = {}
    headers = {
        'authority': 'www.dayfund.cn',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'Hm_lvt_c778c7d65526df5fd97b5496ac256a50=1625629692; Hm_lpvt_c778c7d65526df5fd97b5496ac256a50=1625632163',
        'if-modified-since': 'Wed, 07 Jul 2021 03:50:00 GMT'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    json_text = response.text
    txt = re.findall("<td>.*?</td>", json_text)[9:289]
    for i in range(0, len(txt)):
        if i % 7 == 0:
            code = str(txt[i+1]).replace("<td>", "").replace("</td>", "")
            print(code)
            date = str(txt[i]).replace("<td>", "").replace("</td>", "")
            print(date)
            list1 = fundData.objects.all().filter(fundcode=code, jzrq=date)
            if len(list1) == 0:
                # 写入前查询数据是否存在
                try:
                    funddata = fundData()
                    funddata.jzrq = str(txt[i]).replace("<td>", "").replace("</td>", "")
                    funddata.fundcode = str(txt[i+1]).replace("<td>", "").replace("</td>", "")
                    funddata.name = str(txt[i+2]).replace("<td>", "").replace("</td>", "")
                    funddata.sjjz = str(txt[i+3]).replace("<td>", "").replace("</td>", "")
                    funddata.save()
                except:
                    return JsonResponse({"code": -1, "data": "失败"})
                i += 7
            else:
                return JsonResponse({"code": 0, "data": "成功"})
    return JsonResponse({"code": 0, "data": "成功"})