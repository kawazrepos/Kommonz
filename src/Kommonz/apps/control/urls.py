from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from views import ControlView


urlpatterns = patterns('',
    url(r'^/?$',     login_required(ControlView.as_view()), name='control_main'),
)
