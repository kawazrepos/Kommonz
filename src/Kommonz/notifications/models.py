from auth.models import KommonzUser
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from materials.models.base import Material
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



# signal test below

def my_callback(sender, **kwargs):
    if kwargs.get('created', None):
        print kwargs
        print "----------Request finished!----------"

post_save.connect(my_callback, sender=Message)

@receiver(post_save, sender=Material)
def my_material_callback(sender, **kwargs):
    print kwargs
    print "----------Request finished!----------"
