# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.db import models
from django.utils.translation import ugettext as _
from utils.ffmpeg import get_playtime
from ..models import Material
from ..managers import MaterialManager

class Audio(Material):
    """
        Model for Audio material.
    """
    
    play_time = models.PositiveSmallIntegerField(_('Play Time'), editable=False, default=0)
    
    objects = MaterialManager()

    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Audio')
        verbose_name_plural = _('Audios')

    def save(self, *args, **kwargs):
        if not self.play_time:
            self.play_time = int(get_playtime(self.file.path))
        return super(Audio, self).save(*args, **kwargs)
