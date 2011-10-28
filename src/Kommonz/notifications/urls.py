from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from notifications.views import NotificationListView


urlpatterns = patterns('',
    url(r'^/?$',login_required(NotificationListView.as_view()),name='notifications_notification_list'),
    )
