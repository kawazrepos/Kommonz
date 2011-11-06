# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'
from piston.handler import BaseHandler
from piston.utils import rc, validate, throttle
from ..models.base import Material
from mappers import MaterialMapper

class MaterialHandler(BaseHandler):
    allowed_method = ('GET', 'DELETE', )
    model          = Material
    
    def read(self, request, pk):
        material = self.model.objects.get(pk=pk)
        mapper = MaterialMapper(material)
        return mapper.as_dict()
            
    def delete(self, request, pk):
        """not implemented"""
        return rc.FORBIDDEN
