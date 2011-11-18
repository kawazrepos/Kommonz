# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.db import models
from django.utils.translation import ugettext as _
from ..models import Material
from ..managers import MaterialManager

class Audio(Material):
    """
        Model for Audio material.
    """
    
    play_time = models.PositiveSmallIntegerField(_('Play Time'))
    
    objects = MaterialManager()

    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Audio')
        verbose_name_plural = _('Audios')
