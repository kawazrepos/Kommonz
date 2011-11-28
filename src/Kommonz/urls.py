from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from apps.index.views import IndexView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/',           include('django.contrib.admindocs.urls'),         name='admin_doc'),
    url(r'^admin/',               include(admin.site.urls),                         name='admin'),
<<<<<<< HEAD
    url(r'^control/',             include('Kommonz.apps.control.urls')),
    url(r'^categories/',          include('Kommonz.apps.categories.urls')),
    url(r'^registration/',        include('Kommonz.apps.registration.urls')),
    url(r'^materials/',           include('Kommonz.apps.materials.urls')),
    url(r'^messages/',            include('Kommonz.apps.messages.urls')),
    url(r'^notifications/',       include('Kommonz.apps.notifications.urls')),
    url(r'^reports/',             include('Kommonz.apps.reports.urls')),
    url(r'^searches/',            include('Kommonz.apps.searches.urls')),
    url(r'^users/',               include('Kommonz.apps.auth.urls')),
    url(r'^$',                    IndexView.as_view(), name='index')
=======
    url(r'^registration/',        include('Kommonz.registration.urls')),
    url(r'^materials/',           include('Kommonz.materials.urls')),
    url(r'^messages/',            include('Kommonz.messages.urls')),
    url(r'^list/',                include('Kommonz.list.urls')),
    url(r'^users/(?P<pk>\d+)/',   UserDetailView.as_view(), name="user_detail"),
    url(r'^$',                    TemplateView.as_view(template_name='index.html'), name='index')
>>>>>>> コメント
)

from django.conf import settings
if settings.DEBUG:
    import os.path
    document_root = lambda x: os.path.join(os.path.dirname(__file__), x)
    urlpatterns += patterns('django.views.static',
        (r'^favicon.ico$',              'serve', {'document_root': document_root('../../static'), 'path': 'favicon.ico'}),
        (r'^apple-touch-icon.png$',     'serve', {'document_root': document_root('../../static'), 'path': 'apple-touch-icon.png'}),
        (r'^css/(?P<path>.*)$',         'serve', {'document_root': document_root('../../static/css')}),
        (r'^javascript/(?P<path>.*)$',  'serve', {'document_root': document_root('../../static/javascript')}),
        (r'^image/(?P<path>.*)$',       'serve', {'document_root': document_root('../../static/image')}),
        (r'^storage/(?P<path>.*)$',     'serve', {'document_root': document_root('../../static/storage')}),
    )
