# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.functional import lazy
from django.views.generic import ListView
from apps.categories.models import Category


lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

urlpatterns = patterns('',
    url(r'^/?$',     ListView.as_view(model = Category),   name='categories_material_list'),
)