from django.db import models
from django.utils.translation import ugettext as _
from fields.ccfield.models import CreativeCommonsField
from django.core.exceptions import ValidationError


class License(models.Model):
    u"""
    License
    """
    
    label        = models.CharField(_('Label'), max_length=32)
    description  = models.TextField(_('Description'))


    class Meta:
        app_label           = 'materials'
        verbose_name        = _('License')
        verbose_name_plural = _('Licenses')
        
    def __unicode__(self):
        return self.label 


class CreativeCommons(models.Model):
    u"""
    CreativeCommons http://en.wikipedia.org/wiki/Creative_Commons
    """

    commons       = CreativeCommonsField(_('Creative Commons'))
    material      = models.OneToOneField('Material', verbose_name=_('Creative Commons'), parent_link=True)
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Creative Commons')
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self._get_commons_description()
    
    def _get_commons_description(self):
        nc, nd, sa = self.commons.noncommerical, self.commons.no_derivative, self.commons.share_alike
        if not nd:
            return 'CC BY' if not nc else 'CC BY-NC'
        elif not nd and sa:
            return 'CC BY-SA' if not nc else 'CC-BY-NC-SA'
        elif nd:
            return 'CC BY-ND' if not nc else 'CC BY-NC-ND'
        
    def clean(self):
        if self.commons.no_derivative and self.commons.share_alike:
            raise ValidationError(_('''can not set 'Share Alike' and 'Not Derivative Works' together.'''))
        return super(CreativeCommons, self).clean()