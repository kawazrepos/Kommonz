from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from qwert.middleware.threadlocals import request as get_request
from auth.models import KommonzUser

class Message(models.Model):
    u"""Message object a user sends or receives"""
    
    label           = models.CharField(_('Subject'), max_length=255)
    user_from       = models.ForeignKey(KommonzUser, verbose_name=_('Sender'), 
                                         related_name="sent_messages", editable=False)
    user_to         = models.ForeignKey(KommonzUser, verbose_name=_('Reciver'), related_name="received_messages")
    read            = models.BooleanField(_('Has already read'), default=False)
    created_at      = models.DateTimeField(_('Sent at'), auto_now_add=True)
    body            = models.TextField(_('Body'))
    
    class Meta:
        app_label           = 'messages'
        ordering            = ('-created_at',)
        verbose_name        = _('Message')
        verbose_name_plural = _('Messages')
        
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
            # if guest sender allowed, erase this statement and set self.user_from as guestuser
            raise ValidationError(_('''can not send message without authenticate'''))
        return super(Message, self).clean()

    def modify_object_permission(self, mediator, created):
        mediator.viewer(self, self.user_to)
        mediator.editor(self, self.user_from)
        mediator.reject(self, None)
        mediator.reject(self, 'anonymous')
