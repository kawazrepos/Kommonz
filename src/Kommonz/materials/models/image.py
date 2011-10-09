# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.db import models
from django.utils.translation import ugettext as _
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

    def _create_thumbnail(self):
        """Create thumbnail from image and return that's path."""
        # implement this
        #return filepath