
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                                  actions.List.as_view(),          name='board_task_list'),
    url(r'^update/(?P<id>([0-9]+))$',               actions.Update.as_view(),        name='board_task_update'),
    url(r'^create$',                                actions.Create.as_view(),        name='board_task_create'),
    url(r'^add_cmt$',                               actions.AddComment.as_view(),    name='board_task_create'),
    url(r'^add_tag$',                               actions.AddTag.as_view(),        name='board_task_create'),
    url(r'^update_rating$',                         actions.UpdateRating.as_view(),  name='board_task_update'),
    url(r'^change_stage$',                          actions.ChangeStage.as_view(),   name='board_task_change_stage'),
    url(r'^bulk_delete$',                           actions.BulkDelete.as_view(),    name='board_task_bulk_delete'),
    url(r'^delete_tag$',                            actions.DeleteTag.as_view(),    name='board_task_delete_tag'),
]
