# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url, include
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.functional import lazy
from django.views.generic import ListView
from models.base import Material
from views.edit import MaterialDetailView, MaterialCreateView, MaterialUpdateView, MaterialFileCreateView
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

urlpatterns = patterns('',
    url(r'^api/',                 include('Kommonz.apps.materials.api.urls')),
    url(r'^(?P<pk>\d+)/$',        MaterialDetailView.as_view(),                 name="materials_material_detail"),
    url(r'^(?P<pk>\d+)/update/$', MaterialUpdateView.as_view(),                 name="materials_material_update"),
    url(r'^create/?$',            MaterialFileCreateView.as_view(),             name='materials_material_file_create'),
    url(r'^create/form/?$',       MaterialCreateView.as_view(),                 name='materials_material_create'),
    url(r'^/?$',                  ListView.as_view(model=Material),             name='materials_material_list'),
)
