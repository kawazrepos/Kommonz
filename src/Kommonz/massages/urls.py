from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from massages.views import MassageListView, MassageDetailView, MassageCreateView


urlpatterns = patterns('',
    url(r'^inbox$',         login_required(MassageListView.as_view(template_name="massages/massage_inbox.html")),
        name='massages_massage_inbox'),
    url(r'^outbox$',        login_required(MassageListView.as_view(template_name="massages/massage_outbox.html")),
        name='massages_massage_outbox'),
    url(r'^create$',        login_required(MassageCreateView.as_view()), name='massages_massage_create'),                   
    url(r'^(?P<pk>\d+)/$',  login_required(MassageDetailView.as_view()), name="massages_massage_detail"),
)
