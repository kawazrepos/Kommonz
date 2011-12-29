from django import template
from apps.materials.models import Material

register = template.Library()


@register.tag('render_kero')
def do_render_kero(parser, token):
    try:
        tag_name, preposition, material = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return RenderKeroNode(material)

    
class RenderKeroNode(template.Node):
    def __init__(self, material_to_be_formatted):
        self.material_to_be_formatted = template.Variable(material_to_be_formatted)

    def render(self, context):
        try:
            material = self.material_to_be_formatted.resolve(context)
            if isinstance(material, Material):
                return material.kero.render_html
            else:
                raise template.TemplateSyntaxError("render_kero tag's second argument should be material instance")
        except template.VariableDoesNotExist:
            return ''
