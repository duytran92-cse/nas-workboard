
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^$',                    actions.Summary.as_view(),     name='summary_view'),
]
