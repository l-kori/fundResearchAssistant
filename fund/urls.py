from django.conf.urls import url
from fundPlan import views
urlpatterns = [
    # 获取基金信息
    url(r'^getFundData/', views.getFundData),
    url(r'^addFundList/', views.addFundList),
    url(r'^fundlist/', views.fundlist),
    url(r'^historicalData/', views.historicalData),
    url(r'^synchronousData/', views.synchronousData),
]
