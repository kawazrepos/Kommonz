# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.functional import lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from models import Category
from views import CategoryListView


lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

urlpatterns = patterns('',
    url(r'^/?$',             CategoryListView.as_view(),           name='categories_category_list'),
    url(r'^(?P<pk>\d+)/$',   DetailView.as_view(model = Category), name='categories_category_detail'),
)