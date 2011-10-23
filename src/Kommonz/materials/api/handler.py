# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'
from piston.handler import BaseHandler
from piston.utils import rc, validate, throttle
from bpmappers import RawField
from ..models.base import Material

class MaterialHandler(BaseHandler):
    allowed_method = ('GET', 'POST', 'DELETE', )
    model          = Material
    fields         = (
                      'pk',
                      'label',
                      ('author', ('pk', 'username', 'nickname', 'icon')),
                      'description',
                      'created_at',
                      'updated_at',
                      'pv',
                      'download',
                      'file__path'
    )
    
    def read(self, request, pk):
        material = self.model.objects.get(pk=pk)
        return material
    
    def create(self, request):
        if request.user.is_authenticated():
            instance = self.model.objects.create_material
            
    def delete(self, request, pk):
        """not implemented"""
        return rc.FORBIDDEN