# -*- coding: utf-8 -*-
from Kommonz.materials.views import MaterialDetailView
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.views.generic import CreateView
from models.base import Material
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$',  MaterialDetailView.as_view(), name="materials_material_detail"),
    url(r'^create$',        CreateView.as_view(model=Material), name='materials_material_create'),
)