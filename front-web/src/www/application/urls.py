from django.conf.urls import include, url

urlpatterns = [
    url(r'^$',                                                 include('application.modules.dashboard.urls')),
    url(r'^statistics/',                                       include('application.modules.statistics.urls')),		#link to statistics page
    url(r'^board/',                                            include('application.modules.board.urls')),
    url(r'^queue/',                                            include('application.modules.queue.urls')),
    url(r'^report/',                                           include('application.modules.report.urls')),
    url(r'^file_upload/',                                      include('application.modules.file_upload.urls')),
    url(r'^search/',                       					   include('application.modules.search.urls')),
]
