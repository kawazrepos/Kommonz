from django.template.context import Context
from django.template.loader import get_template, get_template_from_string
from notifications.models import Notification


def create_template_notification(user, template_filename):
    template_path = 'notifications/template_notifications/' + template_filename
    template = get_template(template_path)
    if template:
        create_object_dict = {'user' : user}
        context = Context(create_object_dict.copy())
        label_loader = get_template_from_string('{% extends "' + template_path + '" %}{% block label %}{% endblock %}')
        body_loader = get_template_from_string('{% extends "' + template_path + '" %}{% block body %}{% endblock %}')
        create_object_dict.update({'label' : label_loader.render(context), 'body' : body_loader.render(context)})
        notification = Notification.objects.create(**create_object_dict)
        notification.save()
