from django.conf.urls import include, url

urlpatterns = [
    url(r'^user/',                           include('application.modules.user.urls')),
    url(r'^board/',                          include('application.modules.board.urls')),
    url(r'^board_category/',                 include('application.modules.board_category.urls')),
    url(r'^board_stage/',                    include('application.modules.board_stage.urls')),
    url(r'^board_tag/',                      include('application.modules.board_tag.urls')),
    url(r'^board_goal/',                     include('application.modules.board_goal.urls')),
    url(r'^board_story/',                    include('application.modules.board_story.urls')),
    url(r'^board_event/',                    include('application.modules.board_event.urls')),
    url(r'^queue/',                          include('application.modules.queue.urls')),
    url(r'^queue_request/',                  include('application.modules.queue_request.urls')),
    url(r'^user_monthly_performance/',       include('application.modules.user_monthly_performance.urls')),
    url(r'^statistics/',       				 include('application.modules.statistics.urls')),
    url(r'^search/',                         include('application.modules.search.urls')),
]
