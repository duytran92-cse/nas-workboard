from django.conf.urls import include, url

urlpatterns = [
    url(r'^$',                                  include('application.modules.dashboard.urls')),
    url(r'^board/',                             include('application.modules.board.urls')),
    url(r'^queue/',                             include('application.modules.queue.urls')),
    url(r'^user/',                              include('application.modules.user.urls')),
    url(r'^user_monthly_performance/',          include('application.modules.user_monthly_performance.urls')),
]
