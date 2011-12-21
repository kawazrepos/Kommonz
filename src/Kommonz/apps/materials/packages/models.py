# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
import re
import zipfile
from django.db import models
from django.utils.translation import ugettext as _
from ..models import Material, MaterialFile
from ..managers import MaterialManager

class Package(Material):
    """
    Model for material collections.
    """

    materials = models.ManyToManyField('Material', verbose_name=_("materials"), related_name="packages", null=True, blank=True, editable=False)
    
    objects = MaterialManager()
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Package')
        verbose_name_plural = _('Packages')

    def save(self, *args, **kwargs):
        obj = super(Package, self).save(*args, **kwargs)
        if self.materials.count() == 0:
            self.extract_package()
        return obj

    def extract_package(self, files=None, recursive=False):
        """
        Extract package and create Material model from each files.
        Args
            files(optional)
                it contains pathes of include files.
                Material model objects will be created from files in this list.
            recursive(optional)
                if true, it will create other packages from files in inner directories.
        """
        # on OSX archive contains "__MACOSX" directory.
        ignores = []
        archive = zipfile.ZipFile(self.file.path, "r")
        if archive.namelist()[0].endswith('/'):
            root_dir = archive.namelist()[0]
        def _is_ignore_file(name):
            filename = os.path.basename(name)
            return (files and not name in files) or name.startswith('__MACOSX') or name in ignores or filename.startswith('.')
        archive_root_path = os.path.join(os.path.dirname(self.file.path))
        archive_root_name = os.path.join(os.path.dirname(self.file.name))
        if not os.path.exists(archive_root_path):
            os.mkdir(archive_root_path)
        for name in archive.namelist():
            filename = os.path.basename(name)
            upload_path = os.path.join(archive_root_path, os.path.dirname(name), filename)
            upload_name = os.path.join(archive_root_name, os.path.dirname(name), filename)
            if _is_ignore_file(name):
                # ignore __MACOSX junk and dotfiles.
                continue
            elif name.endswith('/'): # if 'name' is directory
                if not os.path.exists(os.path.join(archive_root_path, name)):
                    os.mkdir(os.path.join(archive_root_path, name))
                if recursive and not name == root_dir:
                    sub_files = [re.sub(r'^%s' % name, '', path) for path in archive.namelist() if path.startswith(name) and not _is_ignore_file(path) and not path == name and not path == root_dir]
                    file_path = os.path.join(upload_path, '%s.zip' % os.path.basename(name[:-1]))
                    file_name = os.path.join(upload_name, '%s.zip' % os.path.basename(name[:-1]))
                    raw_file = open(file_path, 'w+b')
                    sub_archive = zipfile.ZipFile(raw_file, 'w', zipfile.ZIP_DEFLATED)
                    for path in sub_files:
                        sub_archive.writestr(filename, archive.read(os.path.join(name, path)))
                    sub_archive.close()
                    raw_file.close()
                    material_file = MaterialFile.objects.create(file=file_name)
                    sub_package = Material.objects.create(
                        label=filename,
                        _file=material_file,
                        description=self.description,
                        author=self.author,
                        category=self.category
                    )
                    sub_package.extract_package(recursive=True)
                    self.materials.add(sub_package)
                    map(lambda material : self.materials.add(material), sub_package.materials.iterator())
                    ignores += sub_files
            else: # if 'name' is file
                # package files will be saved in /storage/materials/username/packagename/path/to/file/filename/filename.ext
                file_path = os.path.join(upload_path, filename)
                file_name = os.path.join(upload_name, filename)
                if not filename: continue
                if not os.path.exists(upload_path):
                    os.mkdir(upload_path)
                raw_file = open(file_path, 'w+b')
                raw_file.write(archive.read(name))
                raw_file.close()
                material_file = MaterialFile.objects.create(file=file_name)
                material = Material.objects.create(
                    label=filename,
                    _file=material_file,
                    description=self.description,
                    author=self.author,
                    category=self.category
                )
                self.materials.add(material)
        self.save()
