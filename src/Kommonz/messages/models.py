from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from qwert.middleware.threadlocals import request as get_request
from auth.models import KommonzUser


class Message(models.Model):
    u"""Message object a user sends or receives"""
    
    label           = models.CharField(_('subject'), max_length=255)
    user_from       = models.ForeignKey(KommonzUser, verbose_name=_('user this message sent from'), 
                                         related_name="message_from", editable=False)
    user_to         = models.ForeignKey(KommonzUser, verbose_name=_('user this message sent to'), related_name="message_to")
    read            = models.BooleanField(_('has already read'), default=False)
    created_at      = models.DateTimeField(_('datetime sent'), auto_now_add=True)
    body            = models.TextField(_('body of message'))
    
    class Meta:
        app_label           = 'messages'
        ordering            = ('-created_at',)
        verbose_name        = _('Message')
        verbose_name_plural = _('Messages')
        
    def __unicode__(self):
        return self.label
    
    #@models.permalink
    def get_absolute_url(self):
        return "/messages/%i/" % self.id
    
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
        
