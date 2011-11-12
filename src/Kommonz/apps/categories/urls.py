# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from views import CategoryListView
from apps.categories.views import CategoryDetailView


urlpatterns = patterns('',
    url(r'^/?$',             CategoryListView.as_view(),           name='categories_category_list'),
    url(r'^(?P<pk>\d+)/$',   CategoryDetailView.as_view(),         name='categories_category_detail'),
)