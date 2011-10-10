# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.views.generic import CreateView
from models.base import Material
lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

urlpatterns = patterns('',
    url(r'^create$',        CreateView.as_view(model=Material), name='materials_material_create'),
)