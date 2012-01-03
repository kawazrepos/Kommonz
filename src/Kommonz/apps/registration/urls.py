# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/08'

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse
from django.utils.functional import lazy
from django.views.generic import TemplateView
lazy_reverse = lambda name=None, *args : lazy(reverse, str)(name, args=args)

urlpatterns = patterns('',
    url(r'^',              include('social_auth.urls')),
    url(r'^login$',        TemplateView.as_view(template_name='registration/login.html'),   name='registration_index'),
    url(r'^logout$',       auth_views.logout, { 'next_page' : lazy_reverse('index') },      name='registration_logout'),
    url(r'^error$',        TemplateView.as_view(template_name='registration/error.html'),   name='registration_error'),
    url(r'^welcome/?$',    TemplateView.as_view(template_name='registration/welcome.html'), name='registration_welcome'),
)
