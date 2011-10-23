from django import template
from messages.models import Message


register = template.Library()

@register.inclusion_tag('notifications/components/message_notification_list.html', takes_context=True)
def message_notification_list(context):
    request = context['request']
    object_list = Message.objects.filter(user_to=request.user, read=False)
    context['object_list'] = object_list
    return context

@register.simple_tag(takes_context=True)
def message_notification_count(context):
    request = context['request']
    return Message.objects.filter(user_to=request.user, read=False).count()
    