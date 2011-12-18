# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from PIL import Image
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import signals
from ..managers import MaterialManager
from ..models import Material

class Image(Material):
    """
    Model for Image material.
    """
    width  = models.PositiveSmallIntegerField(_('Width'), editable=False, default=0)
    height = models.PositiveSmallIntegerField(_('Height'), editable=False, default=0)
    
    objects = MaterialManager()
    
    object_permission_suffix = '_material'

    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Image')
        verbose_name_plural = _('Images')

    def _get_size(self):
        img = Image.open(self.file.path)
        return img.size
    
    def save(self, *args, **kwargs):
        if not self._thumbnail:
            self._thumbnail = self.file.path
            signals.post_save.connect(self._thumbnail.field._create_thumbnails, sender=Image)
        if not self.width or not self.height:
            self.width, self.height = self._get_size()
        return super(Image, self).save(*args, **kwargs)
