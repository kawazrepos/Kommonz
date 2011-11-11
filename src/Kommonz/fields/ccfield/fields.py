# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'
from django.forms import MultiValueField, fields

from widgets import CreativeCommonsWidget
from types import CreativeCommons

class CreativeCommonsField(MultiValueField):
    widget          = CreativeCommonsWidget
    
    def __init__(self, *args, **kwargs):
        field_list = (
            fields.BooleanField(),
            fields.BooleanField(),
            fields.BooleanField(),
        )
        if 'query_field_id' in kwargs:
            kwargs['widget'] = CreativeCommonsWidget(query_field_id=kwargs.pop('query_field_id'))

        super(CreativeCommonsField, self).__init__(field_list, *args, **kwargs)
        
    def compress(self, data_list):
        if not data_list:
            return ''
        return CreativeCommons(data_list[0], data_list[1], data_list[2])