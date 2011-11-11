from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from views import NotificationListView, NotificationDetailView


urlpatterns = patterns('',
    url(r'^/?$',             login_required(NotificationListView.as_view()),  name='notifications_notification_list'),
    url(r'^(?P<pk>\d+)/?$',  NotificationDetailView.as_view() ,name='notifications_notification_detail'),
    )
