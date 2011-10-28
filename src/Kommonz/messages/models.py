from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from qwert.middleware.threadlocals import request as get_request
from auth.models import KommonzUser


class Message(models.Model):
    u"""Message object a user sends or receives"""
    PUB_STATES = (
                ('sent',             'sent message'),
                ('deleted',          'deleted message'),
                ('receiver_deleted', 'deleted by receiver'),
                ('sender_deleted',   'deleted by sender'),
        )
    pub_state       = models.CharField(_('publish status'), choices=PUB_STATES, max_length=20)
    label           = models.CharField(_('subject'), max_length=255)
    user_from       = models.ForeignKey(KommonzUser, verbose_name=_('sender'), 
                                         related_name='sent_messages', editable=False)
    user_to         = models.ForeignKey(KommonzUser, verbose_name=_('reciver'), related_name='received_messages')
    read            = models.BooleanField(_('has already read'), default=False)
    created_at      = models.DateTimeField(_('sent at'), auto_now_add=True)
    body            = models.TextField(_('body'))
    
    class Meta:
        app_label           = 'messages'
        ordering            = ('-created_at',)
        verbose_name        = _('message')
        verbose_name_plural = _('messages')
        
    def __unicode__(self):
        return self.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('messages_message_detail', (), { 'pk' : self.pk })
    
    def clean(self):
        request = get_request()
        if request.user.is_authenticated():
            self.user_from = request.user
        else:
            raise ValidationError(_('''can not send message without authenticate'''))
        return super(Message, self).clean()

    def modify_object_permission(self, mediator, created):
        if self.pub_state == 'sent':
            mediator.viewer(self, self.user_to)
            mediator.viewer(self, self.user_from)
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
        elif self.pub_state == 'deleted':
            mediator.reject(self, self.user_to)
            mediator.reject(self, self.user_from)
        elif self.pub_state == 'receiver_deleted':
            mediator.reject(self, self.user_to)
        elif self.pub_state == 'sender_deleted':
            mediator.reject(self, self.user_from)
        else:
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
            
