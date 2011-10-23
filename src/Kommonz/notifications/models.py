from django.db import models
from django.utils.translation import ugettext_lazy as _
from auth.models import KommonzUser

class Notification(models.Model):
    u"""Notification to user"""
    
    TYPE_CHOICES = (
    (u'新着メッセージ', 'new_message'),
    (u'情報未登録素材', 'unfinished_upload'),
    )
    
    label             = models.CharField(_('subject'), max_length=255)
    notification_type = models.CharField(_('type'), choices=TYPE_CHOICES, max_length=255)
    user              = models.ForeignKey(KommonzUser, verbose_name=_('user this notification to'), 
                                          related_name="user", editable=False)
    read              = models.BooleanField(_('has already read'), default=False)
    created_at        = models.DateTimeField(_('datetime created'), auto_now_add=True)
    body              = models.TextField(_('body of notification'))
    
    class Meta:
        app_label           = 'notifications'
        ordering            = ('-created_at',)
        verbose_name        = _('Notification')
        verbose_name_plural = _('Notifications')
        
    def __unicode__(self):
        return self.label
    
    #@models.permalink
    def get_absolute_url(self):
        return "/notifications/%i/" % self.id
    
    def modify_object_permission(self, mediator, created):
        mediator.viewer(self, self.user)
        mediator.reject(self, None)
        mediator.reject(self, 'anonymous')
