import os
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.context import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode
from django.utils.translation import ugettext_lazy as _
from auth.models import KommonzUser
from messages.models import Message


class Notification(models.Model):
    u"""Notification object"""
    
    label           = models.CharField(_('subject'), max_length=255)
    body            = models.TextField(_('body'))
    user_from       = models.ForeignKey(KommonzUser, verbose_name=_('sender'), 
                                         related_name='sent_notifications', editable=False)
    user_to         = models.ForeignKey(KommonzUser, verbose_name=_('reciver'),
                                         related_name='received_notifications')
    read            = models.BooleanField(_('has already read'), default=False)
    created_at      = models.DateTimeField(_('sent at'), auto_now_add=True)
    
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField(_('object id'))
    content_object  = generic.GenericForeignKey()
    
    def __unicode__(self):
        return self.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('notifications_notification_detail', (), { 'pk' : self.pk })


def create_notification(related_object, template_filename, 
                        user_to, user_from=KommonzUser.objects.get(pk=1)):
    template_path = os.path.join('notifications/template_notifications', template_filename)
    template = get_template(template_path)
    if template:
        create_object_dict = {'user_from' : user_from,
                              'user_to' : user_to,
                              'content_type' : ContentType.objects.get_for_model(related_object),
                              'object_id' : related_object.pk}
        context = Context(create_object_dict)
        context.update({'object':related_object})
        
        if len(template.nodelist):
            for block in template.nodelist:
                if isinstance(block, BlockNode) and block.name == 'label':
                    create_object_dict.update({'label' : block.render(context)})
                if isinstance(block, BlockNode) and block.name == 'body':
                    create_object_dict.update({'body' : block.render(context)})
            notification = Notification.objects.create(**create_object_dict)
            notification.save()
    else:
        print "create_notification: template not found"


# signal callbacks below
@receiver(post_save, sender=Message,  dispatch_uid='notifications.models')
def new_message_callback(sender, **kwargs):
    if kwargs.get('created', None):
        instance = kwargs.get('instance', None)
        create_notification(instance, 'new_message.txt', instance.user_to, user_from=instance.user_from)
