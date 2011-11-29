from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from views import ListDetailView, ListListView, ListCreateView, ListDeleteView, ListAddView, ListRemoveView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',                    ListListView.as_view(),     name='lists_list_list'),
    url(r'^(?P<pk>\d+)/$',        ListDetailView.as_view(),   name='lists_list_detail'),
    url(r'^(?P<pk>\d+)/add/$',    ListAddView.as_view(),      name='lists_list_add'),
    url(r'^(?P<pk>\d+)/remove/$', ListRemoveView.as_view(),   name='lists_list_remove'),
    url(r'^(?P<pk>\d+)/delete/$', ListDeleteView.as_view(),   name='lists_list_delete'),
    url(r'^create/$',             ListCreateView.as_view(),   name='lists_list_create'),
)
