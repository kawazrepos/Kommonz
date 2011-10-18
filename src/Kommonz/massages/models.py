from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from qwert.middleware.threadlocals import request as get_request
from auth.models import KommonzUser


class Massage(models.Model):
    u"""Massage object a user sends or receives"""
    
    label           = models.CharField(_('subject'), max_length=255)
    user_from       = models.ForeignKey(KommonzUser, verbose_name=_('user this massage sent from'), 
                                         related_name="massage_from", editable=False)
    user_to         = models.ForeignKey(KommonzUser, verbose_name=_('user this massage sent to'), related_name="massage_to")
    read            = models.BooleanField(_('has already read'), default=False)
    created_at      = models.DateTimeField(_('datetime sent'), auto_now_add=True)
    body            = models.TextField(_('body of massage'))
    
    class Meta:
        app_label           = 'massages'
        ordering            = ('-created_at',)
        verbose_name        = _('Massage')
        verbose_name_plural = _('Massages')
        
    def __unicode__(self):
        return self.label
    
    #@models.permalink
    def get_absolute_url(self):
        return "/massages/%i/" % self.id
    
    def clean(self):
        request = get_request()
        if request.user.is_authenticated():
            self.user_from = request.user
        else:
            # if guest sender allowed, erase this statement and set self.user_from as guestuser
            raise ValidationError(_('''can not send massage without authenticate'''))
        return super(Massage, self).clean()

    def modify_object_permission(self, mediator, created):
        mediator.viewer(self, self.user_to)
        mediator.editor(self, self.user_from)
        mediator.reject(self, None)
        mediator.reject(self, 'anonymous')
        
