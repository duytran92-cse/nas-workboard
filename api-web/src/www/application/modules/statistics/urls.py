
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^board_statistics$',                    handlers.GetBoardStatistics.as_view(),                  name='board_statistics'),
    url(r'^story_in_progress$',                   handlers.GetStoryInProgress.as_view(),                  name='story_in_progress'),
    url(r'^user_statistics$',                     handlers.GetUserStatistics.as_view(),                   name='user_statistics'),

#get instruction demo
    url(r'^instruction_demo$',					  handlers.InstructionDemo.as_view(),					  name='instruction_demo'),
]
