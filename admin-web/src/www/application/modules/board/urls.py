
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^list$',                                     actions.List.as_view(),          name='board_list'),
    url(r'^create$',                                   actions.Create.as_view(),        name='board_create'),
    url(r'^delete/(?P<id>([0-9]+))$',                  actions.Delete.as_view(),        name='board_delete'),
    url(r'^update/(?P<board_id>([0-9]+))$',            actions.Update.as_view(),        name='board_update'),
    url(r'^duplicate/(?P<id>([0-9]+))$',               actions.Duplicate.as_view(),     name='board_duplicate'),

    url(r'^summary/(?P<board_id>([0-9]+))$',           include('application.modules.board.summary.urls')),
    url(r'^detail/(?P<board_id>([0-9]+))/goal/',       include('application.modules.board.goal.urls')),
    url(r'^detail/(?P<board_id>([0-9]+))/tag/',        include('application.modules.board.tag.urls')),
    url(r'^detail/(?P<board_id>([0-9]+))/stage/',      include('application.modules.board.stage.urls')),
    url(r'^detail/(?P<board_id>([0-9]+))/category/',   include('application.modules.board.category.urls')),
    url(r'^detail/(?P<board_id>([0-9]+))/task/',       include('application.modules.board.task.urls')),
]
