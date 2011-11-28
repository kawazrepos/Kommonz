from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from views import ListDetailView, ListListView, ListCreateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',              ListListView.as_view(),     name='lists_list_list'),
    url(r'^(?P<pk>\d+)/$',  ListDetailView.as_view(),   name='lists_list_detail'),
    url(r'^create/$',       ListCreateView.as_view(),   name='lists_list_create'),
    url(r'^ordered$', 'apps.lists.views.List_ordered_by_add_at',  name='lists_list_list_ordered'),
)
