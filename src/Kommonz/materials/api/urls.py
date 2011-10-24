# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.functional import lazy
from piston.resource import Resource
from handlers import MaterialHandler
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

material_handler = Resource(MaterialHandler)

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/$',  material_handler,                 name="materials_api"),
)
