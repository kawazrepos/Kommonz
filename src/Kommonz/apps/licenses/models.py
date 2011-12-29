from django.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from apps.materials.codes.models import Code
from apps.materials.models import Material
from django.contrib.contenttypes.models import ContentType


class LicenseDefinition(models.Model):
    u"""
    License Definition.
    
    If you want to define new type of License model, you have to create that as subclass of this model.
    All objects from this class or subclass are supposed to be created as a fixture.
    """
    label       = models.CharField(_('Label'), max_length=255)
    description = models.TextField(_('Description'))
    
    render_html = models.TextField(_('Render HTML'))
    
    def __unicode__(self):
        return self.label
    
    
class License(models.Model):
    u"""
    License for Materials.
    """
    material      = models.OneToOneField(Material, verbose_name=_('Material'),
                                           related_name='license')
    definition    = models.ForeignKey(LicenseDefinition, verbose_name=_('License Definition'),
                                        related_name='license')

    class Meta:
        verbose_name        = _('License')
        verbose_name_plural = _('Licenses')
        
    def __unicode__(self):
        return 'license of ' + self.material.label
    
    def clean(self):
        if isinstance(self.material, Code):
            print 'code!'
            print ContentType.objects.get_for_model(self.definition)
            if not isinstance(self.definition, CodeLicense):
                
                raise ValidationError(_('''can not set the selected license with this model.'''))
        else:
            print 'material!'
            print ContentType.objects.get_for_model(self.definition)
            if not isinstance(self.definition, CCLicense):
                
                raise ValidationError(_('''can not set the selected license with this model.'''))
        return super(License, self).clean()
            

class CodeLicense(LicenseDefinition):
    u"""
    License for Codes.
    """

    class Meta:
        verbose_name        = _('CodeLicense')
        verbose_name_plural = _('CodeLicenses')


class CCLicense(LicenseDefinition): 
    u"""
    CreativeCommons http://en.wikipedia.org/wiki/Creative_Commons
    """

    class Meta:
        verbose_name        = _('CCLicense')
        verbose_name_plural = _('CCLicenses')
