
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^',                    handlers.Search.as_view(),                   name='search'),
]
