from django.db import models
from django.utils.translation import ugettext_lazy as _
from Kommonz.auth.models import KommonzUser


class Massage(models.Model):
    u"""Massage object a user sends or receives"""
    
    subject         = models.CharField(_('subject'), max_length=255)
    user_from       = models.ForeignKey(KommonzUser, verbose_name=_('user this massage sent from'), 
                                         related_name="massage_from", editable=False)
    user_to         = models.ForeignKey(KommonzUser, verbose_name=_('user this massage sent to'), related_name="massage_to")
    is_already_read = models.BooleanField(_('is already read'), default=False)
    sent_at         = models.DateTimeField(_('datetime sent'), auto_now_add=True)
    body            = models.TextField(_('body of massage'))
    
    class Meta:
        app_label           = 'massages'
        ordering            = ('-sent_at',)
        verbose_name        = _('Massage')
        verbose_name_plural = _('Massages')
        
    def __unicode__(self):
        return self.subject
    
    def get_absolute_url(self):
        return "/massages/%i/" % self.id
    