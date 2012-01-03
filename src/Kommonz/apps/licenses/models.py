from django.db import models
from django.utils.translation import ugettext as _


class License(models.Model):
    u"""
    License Definition.    
    If you want to define new type of License model, you have to create that as subclass of this model.
    All objects from this class or subclass are supposed to be created as a fixture.
    """
    label       = models.CharField(_('Label'), max_length=255)
    description = models.TextField(_('Description'))
    
    render_html = models.TextField(_('Render HTML'))

    class Meta:
        verbose_name        = _('License')
        verbose_name_plural = _('Licenses')
        
    def __unicode__(self):
        return self.label

class CodeLicense(License):
    u"""
    License for Codes.
    """

    class Meta:
        verbose_name        = _('CodeLicense')
        verbose_name_plural = _('CodeLicenses')

class CCLicense(License): 
    u"""
    CreativeCommons http://en.wikipedia.org/wiki/Creative_Commons
    """

    class Meta:
        verbose_name        = _('CCLicense')
        verbose_name_plural = _('CCLicenses')

