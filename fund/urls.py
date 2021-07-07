from django.conf.urls import url
from fundPlan import views
urlpatterns = [
    url(r'^addFundList/', views.addFundList),
    url(r'^fundlist/', views.fundlist),
    url(r'^historicalData/', views.historicalData),
    url(r'^synchronousData/', views.synchronousData),
]
