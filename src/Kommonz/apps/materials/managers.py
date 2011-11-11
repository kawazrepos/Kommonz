# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'
from django.db import models

class MaterialManager(models.Manager):
    def get_file_model(self, filename):
        from utils.filetypes import get_file_model
        return get_file_model(filename)
