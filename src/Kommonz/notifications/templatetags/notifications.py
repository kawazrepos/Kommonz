from django import template
from ..models import Notification

register = template.Library()

@register.simple_tag(takes_context=True)
def notification_count(context):
    request = context['request']
    return Notification.objects.filter(user_to=request.user, read=False).count()
    