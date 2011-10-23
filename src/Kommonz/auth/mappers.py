# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'
from bpmappers import NonKeyField
from bpmappers.djangomodel import ModelMapper
from models import KommonzUser

class KommonzUserMapper(ModelMapper):
    permalink = NonKeyField()
    def filter_permalink(self):
        return self.data.get_absolute_url()
    
    class Meta:
        model  = KommonzUser
        fields = ('pk', 'username', 'nickname', 'icon',)