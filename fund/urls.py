from django.conf.urls import url
from fundPlan import views
urlpatterns = [
    url(r'^addFundList/', views.addFundList),
    url(r'^synchronousData/', views.synchronousData),
]