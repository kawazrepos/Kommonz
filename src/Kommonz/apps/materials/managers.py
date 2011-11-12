# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'
import os
from django.db import models

class MaterialManager(models.Manager):
    def get_file_model(self, filename):
        from utils.filetypes import get_file_model
        return get_file_model(filename)

    def create(self, type_cast=True, *args, **kwargs):
        from models.base import Material, MaterialFile
        material_file = kwargs.get("_file")
        model = self.get_file_model(material_file.file.name)
        if model == Material:
            return super(MaterialManager, self).create(*args, **kwargs)
        return model.objects.create(*args, **kwargs)

class MaterialFileManager(models.Manager):
    def create(self, *args, **kwargs):
        super(MaterialFileManager, self).create(*args, **kwargs)
