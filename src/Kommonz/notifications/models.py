# -*- coding: utf-8 -*-
#
# Author:        tohhy
# Date:          2011/11/04
#
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.context import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode
from django.utils.translation import ugettext_lazy as _
from messages.models import Message
import os


class Notification(models.Model):
    u"""Notification object"""
    
    label           = models.CharField(_('subject'), max_length=255)
    body            = models.TextField(_('body'))
    user_from       = models.ForeignKey(User, verbose_name=_('sender'), 
                                         related_name='sent_notifications', editable=False)
    user_to         = models.ForeignKey(User, verbose_name=_('reciver'),
                                         related_name='received_notifications')
    solved          = models.BooleanField(_('has already solved'), default=False)
    created_at      = models.DateTimeField(_('sent at'), auto_now_add=True)
    
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField(_('object id'))
    content_object  = generic.GenericForeignKey()
    
    def __unicode__(self):
        return self.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('notifications_notification_detail', (), { 'pk' : self.pk })
    
    def modify_object_permission(self, mediator, created):
        mediator.viewer(self, self.user_to)
        mediator.reject(self, None)
        mediator.reject(self, 'anonymous')


def create_notification(related_object, template_filename, 
                        user_to,
                        user_from = None,
                        **kwargs):
    u"""
    Create notification to user_to by template.
    
    Attribute:
        related_object    - object which related to notification
        template_filename - message template filename at notifications/template_notifications/.
                            template should include block label and body, used as message subject and body
        user_to           - User created notification send to
        kwargs            - this dict will be thrown to template as context.
        
    Notice:
        context by default includes user_from and user_to, so you can call it in template
        as {{ user_from }} or {{ user_to }}.
        user_from is by default User whose pk=1.
    
    Usage: 
        create_notification(message_instance, 'new_message.txt', instance.user_to, user_from=instance.user_from)
    """
    if not user_from:
        user_from = User.objects.get(pk=1)
    template_path = os.path.join('notifications/template_notifications', template_filename)
    template = get_template(template_path)
    if template:
        create_object_dict = {'user_from' : user_from,
                              'user_to' : user_to,
                              'content_type' : ContentType.objects.get_for_model(related_object),
                              'object_id' : related_object.pk}
        context = Context(create_object_dict)
        context.update({'object':related_object})
        context.update(kwargs)
        
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
    u"""notification of new message received"""
    if kwargs.get('created', None):
        instance = kwargs.get('instance', None)
        if instance:
            create_notification(instance, 'new_message.txt', instance.user_to, user_from=instance.user_from)
