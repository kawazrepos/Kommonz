# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.utils.translation import ugettext as _
from django.db.models import signals
from ..managers import MaterialManager
from ..models import Material

class Image(Material):
    """
    Model for Image material.
    """
    objects = MaterialManager()
    object_permission_suffix = '_material'

    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Image')
        verbose_name_plural = _('Images')
    
    def save(self, *args, **kwargs):
        if not self._thumbnail:
            self._thumbnail = self.file.path
            thumbnail_field = [field for field in self._meta.fields if field.name == '_thumbnail']
            signals.post_save.connect(thumbnail_field[0]._create_thumbnails, sender=Image)
            signals.post_init.connect(thumbnail_field[0]._set_thumbnails, sender=Image)
        return super(Image, self).save(*args, **kwargs)
