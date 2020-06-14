
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                       handlers.Get.as_view(),                         name='board_stage_get'),
    url(r'^get_next_stage$',            handlers.GetNextStage.as_view(),                name='board_stage_get'),
    url(r'^list$',                      handlers.List.as_view(),                        name='board_stage_list'),
    url(r'^create$',                    handlers.Create.as_view(),                      name='board_stage_create'),
    url(r'^update$',                    handlers.Update.as_view(),                      name='board_stage_update'),
    url(r'^delete$',                    handlers.Delete.as_view(),                      name='board_stage_delete'),
]
