from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from massages.models import Massage
from massages.views import MassageListView


urlpatterns = patterns('',
    url(r'^inbox$',         login_required(MassageListView.as_view(template_name="massages/massage_inbox.html")),
        name='massages_massage_inbox'),
    url(r'^outbox$',        login_required(MassageListView.as_view(template_name="massages/massage_outbox.html")),
        name='massages_massage_outbox'),
    url(r'^create$',        login_required(CreateView.as_view(model=Massage)), name='massages_massage_create'),                   
    url(r'^(?P<pk>\d+)/$',  login_required(DetailView.as_view(model=Massage)), name="massages_massage_detail"),
)
