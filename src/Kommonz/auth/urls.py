from auth.views import UserDetailView, UserUpdateView
from django.conf.urls.defaults import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
#    url(r'^(?P<pk>\d+)/$',   UserDetailView.as_view(), name='auth_user_detail'),
    url(r'^(?P<slug>\w+)/$', UserDetailView.as_view(), name='auth_user_detail'),
    url(r'^config/?$',     login_required(UserUpdateView.as_view()),
        name='auth_user_update'),
    url(r'^welcome/?$',    TemplateView.as_view(template_name="auth/user_welcome.html"),
                           name='auth_user_welcome'),
)