from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Reason(models.Model):
    """
        Model of contravention reason.
    """
    label          = models.CharField(_('Label'), max_length=140)
    description    = models.CharField(_('Description'), max_length=512)
    
    class Meta:
        verbose_name        = _('Reason')
        verbose_name_plural = _('Reasons')
        
    def __unicode__(self):
        return self.label


class Report(models.Model):
    """
        Model of report for contravention.
    """
    reason      = models.ForeignKey(Reason, verbose_name=_('reason'), related_name='reports')
    remarks     = models.TextField(_('remarks'))
    checked     = models.BooleanField(_('Checked'), default=False)
    author      = models.ForeignKey(User, verbose_name=_('Author'), editable=False)
    created_at  = models.DateTimeField(_('created at'), auto_now=True)
    
    class Meta:
        ordering            = ('created_at',)
        verbose_name        = _('Report')
        verbose_name_plural = _('Reports')
        
    def __unicode__(self):
        return self.content_object.__unicode__()

