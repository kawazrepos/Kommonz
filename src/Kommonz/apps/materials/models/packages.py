# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
import zipfile
import shutil
from django.db import models
from django.core.files.base import File
from django.utils.translation import ugettext as _
from base import Material, MaterialFile

class Package(Material):
    """
    Model for material collections.
    """

    materials = models.ManyToManyField('Material', verbose_name=_("materials"), related_name="packages", null=True, blank=True)
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Package')
        verbose_name_plural = _('Packages')

    def save(self, *args, **kwargs):
        super(Package, self).save(*args, **kwargs)
        archive = zipfile.ZipFile(self.file.path, "r")
        original_path = self.file.path
        path = os.path.split(original_path)[0]
        print path
        for info in archive.infolist():
            filename = info.filename.encode('utf-8')
            extracted_file = File(archive.extract(filename))
            material_file = MaterialFile.objects.create(file=extracted_file)
            extracted_path = os.path.split(os.path.join(path, filename))[0]
            if not os.path.exists(extracted_path):
                os.makedirs(extracted_path)
            try:
                dst = open(extracted_path, "w")
                shutil.copyfile(extracted_file, dst)
                material = Material.objects.create(
                        label=filename,
                        _file=material_file,
                        description=self.description,
                        author=self.author,
                        category=self.category
                )
                self.materials.add(material)
            except:
                pass #fail silently
