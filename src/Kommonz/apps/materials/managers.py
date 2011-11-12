# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'
from django.db import models

class MaterialManager(models.Manager):
    def get_file_model(self, filename):
        from utils.filetypes import get_file_model
        return get_file_model(filename)

    # def create(self, cast_enable=True, *args, **kwargs):
    #     if cast_enable:
    #         file_id = kwargs.get("_file_id")
    #         file = models.base.MaterialFile.objects.get(pk=file_id)
    #         model = self.get_file_model(file.path)
    #         return model.objects.create(cast_enable=False, *args, **kwargs)
    #     return super(MaterialManager, self).create(*args, **kwargs)
