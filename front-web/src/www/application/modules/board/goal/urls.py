
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                                  actions.List.as_view(),          name='board_goal_list'),
    url(r'^create$',                                actions.Create.as_view(),        name='board_goal_create'),
    url(r'^update/(?P<id>([0-9]+))$',               actions.Update.as_view(),        name='board_goal_update'),
    url(r'^delete/(?P<id>([0-9]+))$',               actions.Delete.as_view(),        name='board_goal_delete'),
    url(r'^bulk-update$',                           actions.BulkUpdate.as_view(),    name='board_goal_bulk_update'),
]
