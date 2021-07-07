import requests
import time
import re
from fundPlan.models import fundData

def getHistoricalData(code):
    today = time.strftime("%Y-%m-%d", time.localtime())
    url = "https://www.dayfund.cn/fundvalue/"+code+".html?sdate=2021-04-07&edate="+str(today)+""

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
                    re_text = {"code": -1, "data": "失败"}
                    return re_text
                i += 7
            else:
                re_text = {"code": 0, "data": "成功"}
                return re_text
    re_text = {"code": 0, "data": "成功"}
    return re_text