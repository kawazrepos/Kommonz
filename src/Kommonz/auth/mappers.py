# -*- coding: utf-8 -*-
from bpmappers import NonKeyField
from bpmappers.djangomodel import ModelMapper
from django.contrib.auth.models import User
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'

class KommonzUserMapper(ModelMapper):
    url = NonKeyField()
    def filter_url(self):
        return self.data.get_absolute_url()
    
    class Meta:
        model  = User
        fields = ('pk', 'username', 'nickname', 'icon',)