# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import zipfile
import shutil
from django.db import models
from django.utils.translation import ugettext as _
from base import Material

class Package(Material):
    """
    Model for material collections.
    """

    materials = models.ManyToManyField('Material', verbose_name=_("materials"), related_name="packages")
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Package')
        verbose_name_plural = _('Packages')

    def save(self, *args, **kwargs):
        archive = zipfile.ZipFile(self.file.path, "r")
        for file in archive.namelist():
            Material.object
        super(Package, self).save(*args, **kwargs)
