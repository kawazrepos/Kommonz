# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'
from django.conf import settings
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class CreativeCommonsWidget(widgets.MultiWidget):
    is_hidden = True
    class Media:
        css = {}
        js = {}
        
    def __init__(self, attrs=None, query_field_id=''):
        widget = (
                  widgets.HiddenInput(attrs=attrs),
                  widgets.HiddenInput(attrs=attrs),
                  widgets.HiddenInput(attrs=attrs)
        )
        self.query_field_id = query_field_id
        super(CreativeCommonsWidget, self).__init__(widget, attrs)
        
    def decompress(self, value):
        if not value:
            return [0] * 3
        return (value.noncommerical, value.no_derivative, value.share_alike)