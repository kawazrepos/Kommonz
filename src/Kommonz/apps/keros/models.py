from django.db import models
from django.utils.translation import ugettext as _

class Kero(models.Model):
    """
    Kero is a rating system for Materials.
    """
    
    def _get_file_path(self, filename):
        return filename
    
    label       = models.CharField(_('Label'), max_length=32)
    description = models.TextField(_('Description'))
    
    render_html = models.TextField(_('Render HTML'))
    
    class Meta:
        verbose_name        = _('KERO')
        verbose_name_plural = verbose_name
        
    @models.permalink
    def get_absolute_url(self):
        return ('keros_kero_detail', (), { 'pk' : self.pk })
    
    def __unicode__(self):
        return self.label