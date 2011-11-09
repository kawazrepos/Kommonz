# -*- coding: utf-8 -*-
#
# zip.py
# created by giginet on 2011/11/09
#
import os
import zipfile
import exceptions
from cStringIO import StringIO
from django.http import HttpResponse, Http404
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import BaseListView
from ..models.base import Material

class ZipResponse(HttpResponse):
    """
    Zip response class.
    """
    def __init__(self, archive=None, filename="", mimetype="application/zip", *args, **kwargs):
        if archive:
            archive.flush()
            super(ZipResponse, self).__init__(mimetype=mimetype, *args, **kwargs)
            self.__setitem__('Content-Disposition', 'attachment; filename=%s' % filename)
            self.write(archive.getvalue())
        else:
            raise Http404('zip archive is not found.')

class MultipleZipResponseMixin(object):
    """
    A mixin that can be used to zip materials
    """
    template_name = None
    response_class = ZipResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a zip archive with the files.
        """
        pathes = self.get_files()
        temp = self._create_zip(pathes)
        response = self.response_class(
                filename=self.get_archive_name(), 
                archive=temp
        )
        temp.close()
        return response

    def get_files(self):
        """
        Returns a list with file pathes.
        """
        raise exceptions.NotImplementedError('get_files is not implemented.')

    def get_archive_name(self):
        """
        Returns archive name.
        """
        return "test.zip"

    def _create_zip(self, pathes):
        """
        Create temporary zip archive via the given pathes list.
        Returns created file.
        """
        temp = StringIO()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        for path in pathes:
            filename = os.path.basename(path)
            file = open(path, 'r')
            archive.writestr(filename, file.read())
        archive.close()
        return temp

class MultipleMaterialZipResponseMixin(MultipleZipResponseMixin):
    def get_files(self):
        qs = self.get_queryset()
        for material in qs:
            if not isinstance(material, Material):
                raise exceptions.TypeError('MultipleZipResponseMixin only takes materials.Material')
        return [material.file.path for material in qs]

class MaterialZipView(MultipleMaterialZipResponseMixin, BaseListView):
    """
    Generate zip archive from Material queryset.
    """
