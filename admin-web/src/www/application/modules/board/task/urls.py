
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                                  actions.List.as_view(),          name='task_list'),
    url(r'^create$',                                actions.Create.as_view(),        name='task_create'),
    url(r'^update/(?P<id>([0-9]+))$',               actions.Update.as_view(),        name='task_update'),
    url(r'^delete/(?P<id>([0-9]+))$',               actions.Delete.as_view(),        name='task_delete'),    
]
