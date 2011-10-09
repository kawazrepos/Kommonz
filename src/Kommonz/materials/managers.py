# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'

from django.db import models
from Kommonz.materials.utils.filetypes import guess

class MaterialManager(models.Manager):
    def _get_file_class(self, filename):
        '''Return suitable class for file'''
        from models.base import Material
        type = guess(filename)
        if not type or type is 'unknown':
            return Material
        cls_name = type[0].upper() + type[1:] #convert from 'type' to 'Type'
        try:
            print "aaa"
            module = __import__('.'.join(('models', type)), globals(), locals(), ['Code'])
            return getattr(module, cls_name)
        except:
            return Material
    
    def create_material(self, data):
        '''Create Material or it's subclasses model object from mimetype.'''
        cls = self._get_file_class(data['file'].name)
        return cls.objects.create(data)