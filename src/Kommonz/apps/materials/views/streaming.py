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
