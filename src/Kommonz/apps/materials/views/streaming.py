# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/views/streaming.py
# created by giginet on 2011/11/25
#
from django.http import HttpResponse

class StreamingHttpResponse(HttpResponse):
    """
    This class exists to bypass middleware that uses .content.

    See Django bug #6027: http://code.djangoproject.com/ticket/6027

    We override content to be a no-op, so that GzipMiddleware doesn't exhaust
    the FileWrapper generator, which reads the file incrementally.
    """

    def _get_content(self):
        return ""

    def _set_content(self, value):
        pass

    content = property(_get_content, _set_content)

class StreamingResponseMixin(object):
    """
    A Mixin that can be used to render file streaming.
    """
    response_class = StreamingHttpResponse
    
    def render_to_response(self, context, **response_kwargs):
        object = context['object']
        response = self.response_class(object.file)
        response['Content-Type'] = object.mimetype
        response['Content-Length'] = object.file.size
        return response
