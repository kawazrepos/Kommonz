# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/08'

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^', include('social_auth.urls')),
    url(r'^login$',   auth_views.login),
    url(r'^logout/$', auth_views.logout, name='auth_logout'),
)