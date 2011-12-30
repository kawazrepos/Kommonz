from django import template

register = template.Library()

@register.tag('get_tagged_instances')
def get_tagged_instances(parser, token):
    try:
        tag_name, preposition, tag = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly two arguments" % token.contents.split()[0])
    return GetTaggedInstancesNode(tag)

class GetTaggedInstancesNode(template.Node):
    def __init__(self, tag_to_be_formatted):
        self.tag_to_be_formatted = template.Variable(tag_to_be_formatted)

    def render(self, context):
        try:
            tag = self.tag_to_be_formatted.resolve(context)
            from universaltag.models import Tag, TaggedItem
            if isinstance(tag, Tag):
                instances = []
                for item in tag.items.iterator():
                    instances.append(item.content_object)
                context['tagged_instances'] = instances
                return ''
            else:
                raise template.TemplateSyntaxError("get_tagged_instances tag's second argument should be universaltag.models.Tag instance")
        except template.VariableDoesNotExist:
            return ''