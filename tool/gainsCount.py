import traceback

import time
import datetime

from django.db.models import Avg
from django.db.models.aggregates import Sum

from fundPlan.models import fundData,fundList
import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)


# 传入今日涨幅，和自定义涨幅 返回isoperation  0=不操作   1=加仓  2= 减仓
def isoperationfund(account,fundcode,jjzf,customzf):
    # 先查询账号的买入时间是否超过一个月
    buyday = str(fundList.objects.filter(fundcode=fundcode,account=account)[0].buytime)
    end_date = time.strftime("%Y-%m-%d", time.localtime())
    # 买入时间和今天的时间差
    differenceDay = datetime.datetime.strptime(end_date,  "%Y-%m-%d" ).date() - datetime.datetime.strptime(buyday,  "%Y-%m-%d %H:%M:%S" ).date()
    # 是否操作
    isoperation = 0
    # 1、如果今天的收益达到历史平均收益的3倍    ==暴涨
    # 历史平均涨幅
    lspjzf = float(fundData.objects.filter(fundcode = fundcode).aggregate(Avg('jdzjrzf'))['jdzjrzf__avg'])
    if float(jjzf) >= lspjzf*3:
        logging.info(fundcode+"当日达到了历史平均收益的3倍")
        isoperation = 2
        return isoperation
    # 买入时间超过30天 可以进行持仓操作
    if differenceDay.days >=30:
        # # 2、如果一周的收益达到历史平均收益的3倍   ==大幅增长
        now = datetime.datetime.now()
        start = str(now - datetime.timedelta(hours=167, minutes=59, seconds=59))[0:10]
        
        weekpjzf = float(fundData.objects.filter(fundcode = fundcode,jzrq__range=(start, end_date)).aggregate(Sum('jrzf'))['jrzf__sum'])
        if weekpjzf+float(jjzf) >= lspjzf*8:
            logging.info(fundcode+"一周的收益达到历史平均收益的3倍")
            isoperation = 2
            return isoperation
        # 3、收益率达到自定义涨幅（比如50%） 
        # if float(jjzf) >= float(customzf):
        #         isoperation = True
        #         return isoperation
    else:
        logging.info(account + "---"+ fundcode+"---还没到30天，不建议交易")
    return isoperation