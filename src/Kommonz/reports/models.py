from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from Kommonz.auth.models import KommonzUser

class Report(models.Model):
    """
        Model of report for contravention.
    """
    
    content_type   = models.ForeignKey(ContentType, verbose_name='Content Type', related_name="content_type_set_for_%(class)s")
    object_id      = models.PositiveIntegerField('Object ID')
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
    
    checked        = models.BooleanField(_('Checked'), default=False)
    
    author         = models.ForeignKey(KommonzUser, verbose_name=_('Author'), editable=False)
    created_at     = models.DateTimeField(_('created at'), auto_now=True)
    
    class Meta:
        ordering            = ('created_at',)
        verbose_name        = _('Report')
        verbose_name_plural = _('Reports')
        
    def __unicode__(self):
        return self.content_object.__unicode__()

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