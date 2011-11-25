# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/templatetags/preview.py
# created by giginet on 2011/11/25
#
import os
from django import template
from django.template.loader import render_to_string
from django.template import TemplateSyntaxError
from ..utils.filetypes import guess

register = template.Library()

class RenderMaterialPreviewBaseNode(template.Node):
    def __init__(self, material):
        self.material = template.Variable(material)

    def render(self, context):
        material = self.material.resolve(context)
        filename = material.file.name
        type = guess(filename)
        context.push()
        try:
            html = render_to_string(
                    os.path.join(self.template_path, "%s.html" % type), {
                        'material' : material
            })
        except:
            html = ''
        context.pop()
        return html
        
class RenderMaterialPreviewHeadNode(RenderMaterialPreviewBaseNode):
    template_path = r"materials/preview/head/"

class RenderMaterialPreviewNode(RenderMaterialPreviewBaseNode):
    template_path = r"materials/preview/body/"

@register.tag
def render_material_preview_head(parser, token):
    """
    Render javascript and css to render material.
       Syntax:
            {% render_material_preview_head for <material> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if not bits[1] == "for":
            raise TemplateSyntaxError("""Second argument must be 'as'.""")
        return RenderMaterialPreviewHeadNode(bits[2])
    raise TemplateSyntaxError("""%s tag must be '{% render_codemirror code %}' or '{% render_codemirror code as syntax %}'""")

@register.tag
def render_material_preview(parser, token):
    """
    Render code on Codemirror
        Syntax:
            {% render_material_preview for <material> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if not bits[1] == "for":
            raise TemplateSyntaxError("""Second argument must be 'as'.""")
        return RenderMaterialPreviewNode(bits[2])
    raise TemplateSyntaxError("""%s tag must be '{% render_codemirror code %}' or '{% render_codemirror code as syntax %}'""")
