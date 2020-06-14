
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                       handlers.Get.as_view(),                         name='board_category_get'),
    url(r'^list$',                      handlers.List.as_view(),                        name='board_category_list'),
    url(r'^create$',                    handlers.Create.as_view(),                      name='board_category_create'),
    url(r'^update$',                    handlers.Update.as_view(),                      name='board_category_update'),
    url(r'^delete$',                    handlers.Delete.as_view(),                      name='board_category_delete'),
]
