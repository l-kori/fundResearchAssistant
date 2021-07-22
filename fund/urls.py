from django.conf.urls import url
from fundPlan import views
urlpatterns = [
    url(r'^addfundlistt/', views.addFundListt),
    url(r'^addfundlist/', views.addFundList),
    url(r'^removefundlist/', views.removeFundList),
    url(r'^synchronousdata/', views.synchronousData),
    url(r'^userlivedata/', views.userLiveData),
    url(r'^fundtips/', views.fundTips),
    url(r'^fundprofit/', views.fundProfit),
    url(r'^queryfundtocode/', views.queryFundToCode),
    url(r'^mindata/', views.minData),
    url(r'^crawlmindata/', views.crawlMinData),
]