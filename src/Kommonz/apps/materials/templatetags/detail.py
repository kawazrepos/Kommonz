# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/templatetags/detail.py
# created by giginet on 2011/12/19
#
import os
from django import template
from django.template.loader import render_to_string
from django.template import TemplateSyntaxError
from ..utils.filetypes import guess

register = template.Library()

class RenderMaterialDetailBaseNode(template.Node):
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
        
class RenderMaterialDetailHeadNode(RenderMaterialDetailBaseNode):
    template_path = r"materials/detail/head/"

class RenderMaterialDetailNode(RenderMaterialDetailBaseNode):
    template_path = r"materials/detail/body/"

@register.tag
def render_material_detail_head(parser, token):
    """
    Render javascript and css to render material.
       Syntax:
            {% render_material_detail_head for <material> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if not bits[1] == "for":
            raise TemplateSyntaxError("""Second argument must be 'as'.""")
        return RenderMaterialDetailHeadNode(bits[2])
    raise TemplateSyntaxError("""%s tag must be '{% render_codemirror code %}' or '{% render_codemirror code as syntax %}'""")

@register.tag
def render_material_detail(parser, token):
    """
    Render material detail.
        Syntax:
            {% render_material_detail for <material> %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        if not bits[1] == "for":
            raise TemplateSyntaxError("""Second argument must be 'as'.""")
        return RenderMaterialDetailNode(bits[2])
    raise TemplateSyntaxError("""%s tag must be '{% render_codemirror code %}' or '{% render_codemirror code as syntax %}'""")
