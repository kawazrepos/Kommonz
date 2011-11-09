from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from views import UserProfileDetailView, UserUpdateView, UserProfileUpdateView, UserOptionUpdateView


urlpatterns = patterns('',
    url(r'^config/?$',     login_required(UserUpdateView.as_view()),
        name='auth_user_update'),
    url(r'^config/profile/?$',     login_required(UserProfileUpdateView.as_view()),
        name='auth_userprofile_update'),
    url(r'^config/option/?$',      login_required(UserOptionUpdateView.as_view()),
        name='auth_useroption_update'),
    url(r'^welcome/?$',    TemplateView.as_view(template_name="auth/user_welcome.html"),
                           name='auth_user_welcome'),
    url(r'^(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name='auth_user_detail'),
)