from django.contrib.auth.models import Message
from django.template.context import Context
from django.template.loader import get_template, get_template_from_string
from notifications.models import Notification

# message update signal(even has_read) should call this
# this method update notification by status of messages to user
def message_notification(user):
    template_path = 'notifications/template_notifications/message_notifications.html'
    template = get_template(template_path)
    unread_object_list = Message.objects.filter(user_to=user, read=False)
    unread_num = unread_object_list.length
    
    create_object_dict = {'user' : user, 'unread_num':unread_num}
    context = Context(create_object_dict.copy())
    label_loader = get_template_from_string('{% extends "' + template_path + '" %}{% block label %}{% endblock %}')
    body_loader = get_template_from_string('{% extends "' + template_path + '" %}{% block body %}{% endblock %}')
    create_object_dict.update({'label' : label_loader.render(context), 'body' : body_loader.render(context)})
    notification = Notification.objects.
    notification.save()

