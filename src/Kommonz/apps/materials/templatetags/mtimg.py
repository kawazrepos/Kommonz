# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/templatetags/mtimg.py
# created by giginet on 2011/11/22
#

from django import template
from django.db import models
from django.utils.safestring import mark_safe
from ..utils.filetypes import guess

register = template.Library()

class RenderMimeTypeImageFor(template.Node):
    def __init__(self, material):
        self.material = template.Variable(material)
    
    def render(self, context):
        material = self.material.resolve(context)
        filename = material.file.name
        type = guess(filename)
        if type:
            tag = r"""<span class="mtimg mt-%s"></span>""" % type
        else:
            tag = r"""<span class="mtimg unknown"></span>"""
        return mark_safe(tag)

@register.tag
def render_mtimg(parser, token):
    """
    Syntax:
    {% render_mtimg for <object> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if bits[1] != 'for':
            raise template.TemplateSyntaxError("second argument of %s tag must be 'for'" % bits[0])
        return RenderMimeTypeImageFor(bits[2])
