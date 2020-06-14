
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                                  actions.List.as_view(),          name='queue_request_list'),
    url(r'^create$',                                actions.Create.as_view(),        name='queue_request_create'),
    url(r'^delete/(?P<id>([0-9]+))$',               actions.Delete.as_view(),        name='queue_request_delete'),
    url(r'^update/(?P<id>([0-9]+))$',               actions.Update.as_view(),        name='queue_request_update'),
]
