# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
import shutil
from django.db import models
from django.utils.translation import ugettext as _
from fields.thumbnailfield.utils import resize_image, get_thumbnail_filename
from base import Material

class Image(Material):
    """
    Model for Image material.
    """
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Image')
        verbose_name_plural = _('Images')

    def save(self):
        if not self.thumbnail:
            self.thumbnail.storage = self._create_thumbnail()
        return super(Image, self).save()

    def clean(self):
        if not self.thumbnail:
            self.thumbnail = self.file
            self._create_thumbnail(self.thumbnail.path)
        super(Image, self).clean()

    def _create_thumbnail(self, filename):
        """
        Create thumbnail from image and return that's path.
        """
        # implement this
        params_size = ('width', 'height', 'force')
        path, original_filename = os.path.split(filename)
        thumbnail = os.path.join(path, "thumbnail", original_filename)
        for pattern_name, pattern_size in Material.THUMBNAIL_SIZE_PATTERNS.iteritems():
            thumbnail_filename = get_thumbnail_filename(thumbnail, pattern_name)
            pattern_size = dict(map(None, params_size, pattern_size))
            shutil.copyfile(filename, thumbnail_filename)
            resize_image(thumbnail_filename, pattern_size)
        return filename

