from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from qwert.middleware.threadlocals import request as get_request
from apps.materials.models import Material


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
    material    = models.ForeignKey(Material, verbose_name=_('Material'), related_name='reports', editable=False)
    created_at  = models.DateTimeField(_('created at'), auto_now=True)
    
    class Meta:
        ordering            = ('created_at',)
        verbose_name        = _('Report')
        verbose_name_plural = _('Reports')
        
    def __unicode__(self):
        return self.reason.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('index', (), {})

    def clean(self):
        request = get_request()
        if request.user.is_authenticated():
            self.author = request.user
        else:
            raise ValidationError(_('''can not make a report without authenticate'''))
        if request.GET.get('pk', None):
            self.material = Material.objects.get(pk=request.GET.get('pk'))
        return super(Report, self).clean()
