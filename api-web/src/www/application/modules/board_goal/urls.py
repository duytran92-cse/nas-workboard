
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                       handlers.Get.as_view(),                         name='board_goal_get'),
    url(r'^list$',                      handlers.List.as_view(),                        name='board_goal_list'),
    url(r'^get_bulk_update$',           handlers.GetBulkUpdate.as_view(),               name='board_goal_list'),
    url(r'^create$',                    handlers.Create.as_view(),                      name='board_goal_create'),
    url(r'^update$',                    handlers.Update.as_view(),                      name='board_goal_update'),
    url(r'^bulk_update$',               handlers.BulkUpdate.as_view(),                      name='board_goal_update'),
    url(r'^delete$',                    handlers.Delete.as_view(),                      name='board_goal_delete'),
]
