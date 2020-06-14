
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                       handlers.Get.as_view(),                         name='user_get'),
    url(r'^get_by_username$',           handlers.GetByUsername.as_view(),               name='user_get_by_username'),
    url(r'^list$',                      handlers.List.as_view(),                        name='user_list'),
    url(r'^create$',                    handlers.Create.as_view(),                      name='user_create'),
    url(r'^update$',                    handlers.Update.as_view(),                      name='user_update'),
    url(r'^delete$',                    handlers.Delete.as_view(),                      name='user_delete'),
]
