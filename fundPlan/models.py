from django.db import models

class fundData(models.Model):
    # 基金代码
    fundcode = models.CharField(max_length=10, null=False)
    # 基金名字
    name = models.CharField(max_length=30, null=False)
    # 数据日期
    jzrq = models.CharField(max_length=18, null=False)
    #实际净值
    sjjz = models.FloatField(max_length=20, null=False)



class fundList(models.Model):
    account = models.CharField(max_length=10, null=False,default="admin")
    fundcode = models.CharField(max_length=10, null=False)