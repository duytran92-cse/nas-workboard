
from django.conf.urls import include, url
from . import handlers

urlpatterns = [
    url(r'^get$',                       handlers.Get.as_view(),                         name='board_story_get'),
    url(r'^get_logs$',                  handlers.GetLogs.as_view(),                     name='board_story_get'),
    url(r'^get_cmts$',                  handlers.GetComments.as_view(),                 name='board_story_get'),
    url(r'^get_tags$',                  handlers.GetTags.as_view(),                     name='board_story_get'),
    url(r'^get_rating$',                handlers.GetRating.as_view(),                   name='board_story_get'),
    url(r'^list$',                      handlers.List.as_view(),                        name='board_story_list'),
    url(r'^create$',                    handlers.Create.as_view(),                      name='board_story_create'),
    url(r'^add_cmt$',                   handlers.AddComments.as_view(),                 name='board_story_create'),
    url(r'^add_tag$',                   handlers.AddTag.as_view(),                      name='board_story_create'),
    url(r'^update$',                    handlers.Update.as_view(),                      name='board_story_update'),
    url(r'^update_rating$',             handlers.UpdateRating.as_view(),                name='board_story_update'),
    url(r'^change_stage$',              handlers.ChangeStage.as_view(),                 name='board_story_update'),
    url(r'^bulk_delete$',               handlers.BulkDelete.as_view(),                  name='board_story_delete'),
    url(r'^delete$',                    handlers.Delete.as_view(),                      name='board_story_delete'),
    url(r'^delete_tag$',                handlers.DeleteTag.as_view(),                   name='board_story_delete'),
]
