from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from views import KeroListView, KeroDetailView

urlpatterns = patterns('',
    url(r'^$',                 KeroListView.as_view(),   name='keros_kero_list'),
    url(r'^(?P<pk>\d+)/$',     KeroDetailView.as_view(), name='keros_kero_detail'),
)
