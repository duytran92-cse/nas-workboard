
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^home/(?P<board_id>([0-9]+))$',                    actions.Home.as_view(),               name='board_home'),
    url(r'^view_assignment/(?P<board_id>([0-9]+))$',         actions.ViewAssignment.as_view(),     name='board_view_assignment'),
    url(r'^detail/(?P<board_id>([0-9]+))/story/',            include('application.modules.board.story.urls')),
    url(r'^detail/(?P<board_id>([0-9]+))/goal/',             include('application.modules.board.goal.urls')),
    url(r'^detail/(?P<board_id>([0-9]+))/event/',            include('application.modules.board.event.urls')),
]
