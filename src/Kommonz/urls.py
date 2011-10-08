from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/',       include('django.contrib.admindocs.urls')),
    url(r'^admin/',           include(admin.site.urls)),
    url(r'^registrations/',   include('Kommonz.registrations.urls')),
    url(r'^$',                TemplateView.as_view(template_name='index.html'), name='index')
)