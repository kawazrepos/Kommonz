# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'
import os
from django.db import models
from django.core.files.base import File
from querysets import SubclassingQuerySet

class MaterialManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)

    def get_file_model(self, filename):
        from utils.filetypes import get_file_model
        return get_file_model(filename)

    def create(self, type_cast=True, *args, **kwargs):
        from models import Material, MaterialFile
        if not type_cast:
            return super(MaterialManager, self).create(*args, **kwargs)
        material_file = kwargs.get("_file")
        if not isinstance(material_file, MaterialFile):
            f = File(material_file)
            material_file = MaterialFile.objects.create(file=f)
            kwargs.update({"_file" : material_file})
        model = self.get_file_model(material_file.file.name)
        return model.objects.create(type_cast=False, *args, **kwargs)

class MaterialFileManager(models.Manager):
    def create(self, *args, **kwargs):
        super(MaterialFileManager, self).create(*args, **kwargs)
