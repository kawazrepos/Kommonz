from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from lists.views import ListDetailView, ListListView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',              ListListView.as_view(),     name='lists_list_list'),
    url(r'^(?P<pk>\d+)/$',  ListDetailView.as_view(),   name='lists_list_detail'),
    url(r'^ordered$', 'lists.views.List_ordered',     name='lists_list_list_ordered'),
)