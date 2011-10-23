# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'
from django.core.urlresolvers import reverse
from bpmappers import DelegateField, NonKeyField
from bpmappers.djangomodel import ModelMapper
from Kommonz.auth.mappers import KommonzUserMapper
from ..models.base import Material

class MaterialMapper(ModelMapper):
    #author = DelegateField(KommonzUserMapper, 'author')
    url           = NonKeyField()
    thumbnail_url = NonKeyField()
    delete_url    = NonKeyField()
    delete_type   = NonKeyField()
    
    
    def filter_url(self):
        return self.data.get_absolute_url()
    
    def filter_thumbnail_url(self):
        return self.get_thumbnail_url()
    
    def filter_delete_url(self):
        return reverse('materials_api', args=[self.data.pk])
    
    def filter_delete_type(self):
        return 'DELETE'
    
    #thumbnail = ListDelegateField(ThumbnailMapper, 'thumbnail') # not implemented ThumbnailField
    
    class Meta:
        model  = Material
        fields = ('label', 'description', 'file.name', 'created_at.__unicode__', 'updated_at.__unicode__', 'pv', 'download', )