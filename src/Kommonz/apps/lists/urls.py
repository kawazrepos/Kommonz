from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                    ListListView.as_view(),     name='lists_list_list'),
    url(r'^(?P<pk>\d+)/$',        ListDetailView.as_view(),   name='lists_list_detail'),
    url(r'^(?P<pk>\d+)/add/$',    ListAddMaterialView.as_view(),      name='lists_list_add'),
    url(r'^(?P<pk>\d+)/remove/$', ListRemoveMaterialView.as_view(),   name='lists_list_remove'),
    url(r'^(?P<pk>\d+)/update/$', ListUpdateView.as_view(),   name='lists_list_update'),
    url(r'^(?P<pk>\d+)/delete/$', ListDeleteView.as_view(),   name='lists_list_delete'),
    url(r'^(?P<pk>\d+)/zip/$',    ListZipView.as_view(),      name='lists_list_zip'),
    url(r'^create/$',             ListCreateView.as_view(),   name='lists_list_create'),
)
