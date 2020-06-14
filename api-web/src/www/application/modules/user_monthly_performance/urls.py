
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                       handlers.Get.as_view(),                         name='user_monthly_performance_get'),
    url(r'^list$',                      handlers.List.as_view(),                        name='user_monthly_performance_list'),
    url(r'^create$',                    handlers.Create.as_view(),                      name='user_monthly_performance_create'),
    url(r'^update$',                    handlers.Update.as_view(),                      name='user_monthly_performance_update'),
    url(r'^delete$',                    handlers.Delete.as_view(),                      name='user_monthly_performance_delete'),
]
