
from django.conf.urls import include, url

urlpatterns = [
    url(r'^detail/(?P<queue_id>([0-9]+))/request/',            include('application.modules.queue.request.urls')),
]
