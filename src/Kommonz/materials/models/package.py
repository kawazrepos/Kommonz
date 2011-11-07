from django.db import models
from materials.models.base import Material


class Package(models.Model):
    """
        Model for material packages.
    """
    
    materials  = models.ManyToManyField(Material, verbose_name=_('Materials'))
    

    class Meta:
        app_label           = 'packages'
        verbose_name        = _('Package')
        verbose_name_plural = _('Packages')
        
    
    