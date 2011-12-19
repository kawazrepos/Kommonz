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
            if hasattr(material.thumbnail, 'large'):
                html = """<img src="/%(path)s" 
                    width="%(width)dpx" 
                    height="%(height)dpx">""" % {
                        'path' : material.thumbnail.large.name,
                        'width' : material.thumbnail.large.width,
                        'height' : material.thumbnail.large.height
                    }
            else:
                html = ''
        context.pop()
        return html
        
class RenderMaterialPreviewNode(RenderMaterialPreviewBaseNode):
    template_path = r"materials/preview/"

@register.tag
def render_material_preview(parser, token):
    """
    Render material preview
        Syntax:
            {% render_material_preview for <material> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if not bits[1] == "for":
            raise TemplateSyntaxError("""Second argument must be 'as'.""")
        return RenderMaterialPreviewNode(bits[2])
    raise TemplateSyntaxError("""%s tag must be '{% render_codemirror code %}' or '{% render_codemirror code as syntax %}'""")
