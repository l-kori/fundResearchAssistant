from django.db import models

class fundData(models.Model):
    # 基金代码
    fundcode = models.CharField(max_length=10, null=False)
    # 基金名字
    name = models.CharField(max_length=30, null=False)
    # 数据日期
    jzrq = models.DateTimeField(max_length=18, null=False)
    #实际净值
    sjjz = models.FloatField(max_length=20, null=False)
    #今日涨幅
    jrzf = models.FloatField(max_length=20, null=False,default=0)
    # 绝对值涨幅
    jdzjrzf = models.FloatField(max_length=20, null=False,default=0)

class fundList(models.Model):
    account = models.CharField(max_length=10, null=False,default="admin")
    fundcode = models.CharField(max_length=10, null=False)

class fundtipslog(models.Model):
    account = models.CharField(max_length=10, null=False,default="admin")
    fundcode = models.CharField(max_length=10, null=False)
    # 建议的基金涨幅
    jjzf = models.FloatField(max_length=20, null=False,default=0)
    # 建议调仓类型   1=加仓  0=减仓
    warehousetype = models.IntegerField(null=False)