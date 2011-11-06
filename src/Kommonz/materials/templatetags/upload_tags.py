# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/23'
import os
from django import template
from django.template.loaders.filesystem import Loader
from django.conf import settings

register = template.Library()

@register.simple_tag
def upload_js():
    """
        return a jQuery Templates
        ref : http://api.jquery.com/category/plugins/templates/
    """
    path = os.path.join(settings.ROOT, 'templates/materials')
    loader = Loader()
    string, filename = loader.load_template_source('material_uploader_template.html', (path, ))
    return string