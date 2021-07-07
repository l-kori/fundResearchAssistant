import time

import requests
import re

url = "https://www.dayfund.cn/fundvalue/003096.html?sdate=2021-04-07&edate=2021-07-07"

payload={}
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
txt = re.findall("<td>.*?</td>",json_text)[9:289]
count = 1
for i in range(0,len(txt)):
    if i%7==0:
        # str(txt[i]).replace("<td>","").replace("</td>","")
        i+=7
today = time.strftime("%Y-%m-%d", time.localtime())
print(today)