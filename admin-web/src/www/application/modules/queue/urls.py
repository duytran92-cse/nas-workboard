
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                                     actions.List.as_view(),          name='queue_list'),
    url(r'^create$',                                   actions.Create.as_view(),        name='queue_create'),
    url(r'^delete/(?P<id>([0-9]+))$',                  actions.Delete.as_view(),        name='queue_delete'),
    url(r'^update/(?P<queue_id>([0-9]+))$',            actions.Update.as_view(),        name='queue_update'),

    url(r'^detail/(?P<queue_id>([0-9]+))/request/',       include('application.modules.queue.request.urls')),
]
