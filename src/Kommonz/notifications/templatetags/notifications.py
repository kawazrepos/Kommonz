from django import template
from ..models import Notification

register = template.Library()

@register.simple_tag(takes_context=True)
def notification_count(context):
    request = context['request']
    return Notification.objects.filter(user_to=request.user, solved=False).count()
    

@register.inclusion_tag('notifications/components/message_notification_list.html',
                         takes_context=True)
def notification_list(context):
    
    request = context['request']
    
    object_list = Notification.objects.filter(user_to=request.user, solved=False)
    
    context['notification_object_list'] = object_list
                      
    return context
 