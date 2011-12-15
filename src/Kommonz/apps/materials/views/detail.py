# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/views/detail.py
# created by giginet on 2011/11/15
#
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from django.views.decorators.cache import never_cache
from utils.decorators import view_class_decorator
from ..models import Material
from attachment import AttachmentResponseMixin
from streaming import StreamingResponseMixin

class MaterialBaseDetailView(BaseDetailView):
    def get_object(self, queryset=None):
        instance = super(BaseDetailView, self).get_object(queryset)
        return instance.model.objects.get(pk=instance.pk)

class MaterialDetailView(MaterialBaseDetailView, SingleObjectTemplateResponseMixin):
    model = Material
    template_name = "materials/material_detail.html"

@view_class_decorator(never_cache)
class MaterialDownloadView(AttachmentResponseMixin, MaterialBaseDetailView):
    model = Material

    def _get_file_path(self):
        return self.object.file.path

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.download += 1
        self.object.save()
        return super(MaterialDownloadView, self).get(request, *args, **kwargs)

@view_class_decorator(never_cache)
class MaterialPreviewView(StreamingResponseMixin, MaterialBaseDetailView):
    model = Material
