# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
import zipfile
import tempfile
import shutil
from django.db import models
from django.core.files.base import File
from django.utils.translation import ugettext as _
from django.conf import settings
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

    def extract_package(self, files=None, recursive=False):
        """
        Extract package and create Material instance from each files.
        Args
            files(optional)
                it contains pathes of include file.
                Material model objects will created from files in this list.
            recursive(optional)
                if true, it will create other packages from files in inner directories.
        """
        # on OSX archive contains "__MACOSX" directory.
        ignores = ['__MACOSX',]
        archive = zipfile.ZipFile(self.file.path, "r")
        archive_root_path = os.path.join(os.path.dirname(self.file.path))
        if not os.path.exists(archive_root_path):
            os.mkdir(archive_root_path)
        for name in archive.namelist():
            filename = os.path.basename(name)
            if (files and not name in files) or name in ignores:
                continue
            elif filename.startswith('.'):
                # ignore __MACOSX junk and dotfiles.
                continue
            elif name.endswith('/'): # if 'name' is directory
                if not os.path.exists(name):
                    os.mkdir(os.path.join(archive_root_path, name))
                if recursive:
            else: # if 'name' is file
                upload_path = os.path.join(archive_root_path, os.path.dirname(name), filename)
                if not os.path.exists(upload_path):
                    os.mkdir(upload_path)
                file_path = os.path.join(upload_path, filename)
                raw_file = open(file_path, 'w+b')
                raw_file.write(archive.read(name))
                raw_file.close()
                material_file = MaterialFile.objects.create(file=file_path)
                material = Material.objects.create(
                    label=name,
                    _file=material_file,
                    description=self.description,
                    author=self.author,
                    category=self.category
                )
                self.materials.add(material)
        try:
            osxjunk = os.path.join(archive_root_path, '__MACOSX')
            shutil.rmtree(osxjunk)
        except:
            pass
        self.save()
