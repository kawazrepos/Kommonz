from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/',       include('django.contrib.admindocs.urls'),         name='admin_doc'),
    url(r'^admin/',           include(admin.site.urls),                         name='admin'),
    url(r'^registration/',    include('Kommonz.registration.urls')),
    url(r'^$',                TemplateView.as_view(template_name='index.html'), name='index')
)