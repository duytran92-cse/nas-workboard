
from django.conf.urls import include, url
from . import actions

urlpatterns = [
    url(r'^profile$',                   actions.Profile.as_view(),              name='user_profile'),
    url(r'^profile/edit$',              actions.EditProfile.as_view(),          name='user_edit_profile'),
    url(r'^avatar/edit$',               actions.EditAvatar.as_view(),           name='user_edit_avatar'),
    url(r'^change-password$',           actions.ChangePassword.as_view(),       name='user_change_password'),
    url(r'^inbox$',                     actions.Inbox.as_view(),                name='user_inbox'),
]
