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
from ..models import Material, MaterialFile

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
        package_path = self.file.path
        upload_path = os.path.dirname(package_path)
        for name in archive.namelist():
            filename = os.path.basename(name)
            if name.endswith('/'):
                try: # Don't try to create a directory if exists
                    os.mkdir(os.path.join(upload_path, name))
                except:
                    pass
            elif name.startswith('__MACOSX') or filename.startswith('.'):
                # ignore __MACOSX junk and dotfiles.
                continue
            else:
                raw_file = open(os.path.join(upload_path, name), 'wb')
                raw_file.write(archive.read(name))
                raw_file.close()
                raw_file = open(os.path.join(upload_path, name), 'rb')
                file = File(raw_file)
                material_file = MaterialFile.objects.create(file=file)
                self.materials.create(
                    label=name,
                    _file=material_file,
                    description=self.description,
                    author=self.author,
                    category=self.category
                )
                raw_file.close()
        super(Package, self).save(*args, **kwargs)
        try:
            osxjunk = os.path.join(upload_path, '__MACOSX')
            shutil.rmtree(osxjunk)
        except:
            pass

    def _extract_package(self, files=[], recursive=False):
        """
        Extract package and create Material instance from each files.
        Args
            files
                it contains pathes of include file.
            recursive
                if true, it will create other packages from files in inner directories.
        """
