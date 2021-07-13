from django.conf.urls import url
from fundPlan import views
urlpatterns = [
    url(r'^addfundlist/', views.addFundList),
    url(r'^removefundlist/', views.removeFundList),
    url(r'^synchronousdata/', views.synchronousData),
    url(r'^userlivedata/', views.userLiveData),
    url(r'^marketdata/', views.marketData),
]