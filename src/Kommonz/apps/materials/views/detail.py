# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/views/detail.py
# created by giginet on 2011/11/15
#
import os
import urllib
import mimetypes
from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from ..models import Material
from streaming import StreamingResponseMixin

class MaterialBaseDetailView(BaseDetailView):
    def get_object(self, queryset=None):
        instance = super(BaseDetailView, self).get_object(queryset)
        return instance.model.objects.get(pk=instance.pk)

class MaterialDetailView(MaterialBaseDetailView, SingleObjectTemplateResponseMixin):
    model = Material
    template_name = "materials/material_detail.html"

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

class MaterialDownloadView(AttachmentResponseMixin, MaterialBaseDetailView):
    model = Material

    def _get_file_path(self):
        return self.object.file.path

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(MaterialDownloadView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.download += 1
        self.object.save()
        return super(MaterialDownloadView, self).get(request, *args, **kwargs)

class MaterialPreviewView(StreamingResponseMixin, MaterialBaseDetailView):
    model = Material
