# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'

from django.db import models
from Kommonz.materials.utils.filetypes import guess

class MaterialManager(models.Manager):
    def _get_file_class(self, filename):
        '''return suitable class for file'''
        type = guess(filename)
        #convert from 'type' to 'Type'
        cls_name = type[0].upper() + type[1:]
        return __import__('models', globals(), locals(), [cls_name])
    
    def create_material(self, data):
        '''Create Material or it's subclasses model object from mimetype.'''
        cls = self._get_file_class(data['file'].name)
        return cls.objects.create(data)