# -*- coding: utf-8 -*-
#
# src/Kommonz/templatetags/codemirror.py
# created by giginet on 2011/11/19
#
from django import template
from django.template.loader import render_to_string
from django.template import TemplateSyntaxError

register = template.Library()

class RenderCodeMirrorHeadNode(template.Node):
    def render(self, context):
        context.push()
        html = render_to_string("codemirror/head.html", {
            'js_path' : '/javascript/codemirror/',
            'css_path' : '/css/codemirror/'
        })
        context.pop()
        return html

class RenderCodeMirrorNode(template.Node):
    def __init__(self, code, syntax=None):
        self.code = template.Variable(code)
        self.syntax = template.Variable(syntax) if syntax else None

    def render(self, context):
        code = self.code.resolve(context)
        body = code.body
        if self.syntax:
            syntax = self.syntax.resolve(context)
        else:
            syntax = getattr(code, 'syntax', 'undefined')
        syntax = syntax.lower()
        context.push()
        html = render_to_string("codemirror/code.html", {
            'body' : body,
            'syntax' : syntax,
            'cls' : 'codemirror'
        })
        context.pop()
        return html

@register.tag
def render_codemirror_head(parser, token):
    """
    Render javascript and css to render CodeMirror.
       Syntax:
            {% render_codemirror_head %}
    """
    bits = token.split_contents()
    if len(bits) == 1:
        return RenderCodeMirrorHeadNode()
    raise TemplateSyntaxError("%s tag don't takes any arguments." % bits[0])

@register.tag
def render_codemirror(parser, token):
    """
    Render code on Codemirror
        Syntax:
            {% render_codemirror for <code> %}
            {% render_codemirror for <code> as <syntax> %}
    """
    bits = token.split_contents()
    if len(bits) > 2:
        if not bits[1] == "for":
            raise TemplateSyntaxError("""Second argument must be 'for'.""")
    if len(bits) == 3:
        return RenderCodeMirrorNode(bits[2])
    elif len(bits) == 5:
        if not bits[3] == "as":
            raise TemplateSyntaxError("""Fourth argument must be 'as'.""")
        return RenderCodeMirrorNode(bits[1], bits[3])
    raise TemplateSyntaxError("""%s tag must be '{% render_codemirror for code %}' or '{% render_codemirror for code as syntax %}'""")
