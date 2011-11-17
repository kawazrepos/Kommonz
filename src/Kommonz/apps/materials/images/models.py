# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
import shutil
from django.db import models
from django.utils.translation import ugettext as _
from fields.thumbnailfield.utils import create_thumbnail, convert_patterns_dict
from ..managers import MaterialManager
from ..models import Material

class Image(Material):
    """
    Model for Image material.
    """
    
    objects = MaterialManager()

    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Image')
        verbose_name_plural = _('Images')

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            self.thumbnail = self.file
            self._create_thumbnail(self.thumbnail.path)
        return super(Image, self).save(*args, **kwargs)

    def _create_thumbnail(self, filename):
        """
        Create thumbnail from image and return that's path.
        """
        # implement this
        params_size = ('width', 'height', 'force')
        path, original_filename = os.path.split(filename)
        thumbnail = os.path.join(path, "thumbnail", original_filename)
        patterns = convert_patterns_dict(Material.THUMBNAIL_SIZE_PATTERNS)
        create_thumbnail(filename, thumbnail, patterns)
        return filename

