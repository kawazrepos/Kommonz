from django.conf.urls.defaults import patterns, url
from apps.searches.views import SearchResultView


urlpatterns = patterns('',
    url(r'^$',  SearchResultView.as_view(),  name='searches_result'),
)
