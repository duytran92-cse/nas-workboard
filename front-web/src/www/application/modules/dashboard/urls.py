
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.Home.as_view(),     name='dashboard_home')
]
