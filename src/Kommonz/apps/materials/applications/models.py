# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.db import models
from django.utils.translation import ugettext as _
from ..models import Material

class Application(Material):
    """
        Model for Application material.
    """
    
    version = models.CharField(_('Application Version'), max_length=64)
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Application')
        verbose_name_plural = _('Applications')
    
class Platform(models.Model):
    """
        Model for support platform.
    """
    
    label                   = models.CharField(_('Platform Name'), max_length=64)
    version                 = models.CharField(_('Platform Version'), max_length=64)
    application             = models.ForeignKey(Application, verbose_name=_('Application'), related_name='platforms')
    
    class Meta:
        app_label           = 'materials'
        ordering            = ('label', 'version',)
        verbose_name        = _('Platform')
        verbose_name_plural = _('Platforms')
