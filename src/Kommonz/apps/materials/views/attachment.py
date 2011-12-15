# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/views/attachment.py
# created by giginet on 2011/12/15
#
import os
import urllib
import mimetypes
from django.http import HttpResponse
class AttachmentResponseMixin(object):
    """
    A Mixin that can be used to render raw-file as attachment.

    Ref : http://djangosnippets.org/snippets/1710/
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        path = self._get_file_path()
        filename = os.path.basename(path)
        fp = open(path, 'rb')
        response = self.response_class(fp.read())
        fp.close()
        type, encoding = mimetypes.guess_type(filename)
        if not type:
            type = 'application/octet-stream'
        response['Content-Type'] = type
        response['Content-Length'] = str(os.stat(path).st_size)
        if encoding is not None:
            response['Content-Encoding'] = encoding

        agent = self.request.META['HTTP_USER_AGENT']
        if u'webkit' in agent.lower():
            filename_header = 'filename=%s' % filename.encode('utf-8')
        elif u'msie' in agent.lower():
            filename_header = ''
        else:
            filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(filename.encode('utf-8'))
        response['Content-Disposition'] = 'attachment; %s' % filename_header
        return response

    def _get_file_path(self):
        """
        Returns rendering file path.
        """
        raise NotImplementedError('_get_file_path have not implemented.')

