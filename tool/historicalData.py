import traceback

import requests
import time
import re
from fundPlan.models import fundData
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

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
    txt = re.findall("<td>.*?</td>|<td class=\"green\">.*?</td>|<td class=\"red\">.*?</td>", json_text)[9:371]
    print(txt)
    for i in range(0, len(txt)):
        if i % 9 == 0:
            code = str(txt[i+1]).replace("<td>", "").replace("</td>", "")
            date = str(txt[i]).replace("<td>", "").replace("</td>", "")
            list1 = fundData.objects.all().filter(fundcode=code, jzrq=date)
            # 计算20个交易日的平均涨幅
            # ljzf = fundData.objects.aggregate(Avg("jsjz"))
            # 写入前查询数据是否存在
            if len(list1) == 0:
                try:
                    funddata = fundData()
                    funddata.jzrq = str(txt[i]).replace("<td>", "").replace("</td>", "")
                    funddata.fundcode = str(txt[i+1]).replace("<td>", "").replace("</td>", "")
                    funddata.name = str(txt[i+2]).replace("<td>", "").replace("</td>", "")
                    funddata.sjjz = str(txt[i+3]).replace("<td>", "").replace("</td>", "")
                    funddata.jrzf = re.findall("[-+]?([0-9]*\.[0-9]+|[0-9]+)",str(txt[i+8]).replace("<td>", "").replace("</td>", ""))[0]
                    funddata.save()
                    logging.info(code + "----" + date+"同步成功")
                    i += 9
                except Exception as e:
                    logging.info("同步失败，数据库写入失败")
                    logging.error(e)
                    logging.error(traceback.format_exc())
                    re_text = {"code": -1, "data": "失败"}
                    err = "失败"
                    return re_text,err

            else:
                logging.info(code + "----" + date+"数据存在，无需同步")
                re_text = "成功"
                return re_text
    re_text = "成功"
    return re_text


