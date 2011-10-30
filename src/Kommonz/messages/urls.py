from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from messages.views import MessageListView, MessageDetailView, MessageCreateView, MessageDeleteView


urlpatterns = patterns('',
    url(r'^outbox/?$',             login_required(MessageListView.as_view(template_name='messages/message_outbox.html')),
        name='messages_message_outbox'),
    url(r'^create/?$',             login_required(MessageCreateView.as_view()), name='messages_message_create'),
    url(r'^(?P<pk>\d+)/$',         login_required(MessageDetailView.as_view()), name='messages_message_detail'),
    url(r'^(?P<pk>\d+)/delete/?$', login_required(MessageDeleteView.as_view()), name='messages_message_delete'),
    url(r'^$',                     login_required(MessageListView.as_view(template_name='messages/message_inbox.html')),
        name='messages_message_list'),
)
