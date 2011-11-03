# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'
from django.core.urlresolvers import reverse
from bpmappers import DelegateField, NonKeyField
from bpmappers.djangomodel import ModelMapper
from Kommonz.auth.mappers import KommonzUserMapper
from ..models.base import Material, MaterialFile

class MaterialMapper(ModelMapper):
    #author = DelegateField(KommonzUserMapper, 'author')
    url           = NonKeyField()
    thumbnail_url = NonKeyField()
    form_url      = NonKeyField()
    delete_url    = NonKeyField()
    delete_type   = NonKeyField()
    
    def filter_url(self):
        return self.data.get_absolute_url()
    
    def filter_thumbnail_url(self):
        return self.data.get_thumbnail_url()
    
    def filter_form_url(self):
        return reverse('materials_material_inline_update', args=[self.data.pk,])
    
    def filter_delete_url(self):
        return reverse('materials_api', args=[self.data.pk,])
    
    def filter_delete_type(self):
        return 'DELETE'
    
    #thumbnail = ListDelegateField(ThumbnailMapper, 'thumbnail') # not implemented ThumbnailField
    
    class Meta:
        model  = Material
        fields = ('label', 'description', 'file.name', 'created_at.__unicode__', 'updated_at.__unicode__', 'pv', 'download', )

class MaterialFileMapper(ModelMapper):
    filename = NonKeyField()
    filetype = NonKeyField()

    def filter_filename(self):
        import os
        return os.path.split(self.data.file.name)[1]

    def filter_filetype(self):
        return self.data.extension

    class Meta:
        model  = MaterialFile
        fields = ('id',)
