# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.functional import lazy
from models.base import Material
from views import MaterialDetailView, MaterialCreateView
from forms import MaterialForm
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$',  MaterialDetailView.as_view(),                 name="materials_material_detail"),
    url(r'^create$',        login_required(MaterialCreateView.as_view()), name='materials_material_create'),
)