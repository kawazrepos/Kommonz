from auth.views import UserDetailView
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$', UserDetailView.as_view(), name='auth_user_detail'),
)