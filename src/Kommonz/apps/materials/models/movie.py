# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.db import models
from django.utils.translation import ugettext as _
from base import Material

class Movie(Material):
    """
        Model for Movie material.
    """
    
    play_time = models.PositiveSmallIntegerField(_('Play Time'))
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Movie')
        verbose_name_plural = _('Movies')