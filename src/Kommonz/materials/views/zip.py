# -*- coding: utf-8 -*-
#
# zip.py
# created by giginet on 2011/11/09
#
import tmpfile
import zipfile
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import BaseListView

class MultipleMaterialZipResponseMixin(TemplateResponseMixin):
    """
        A mixin that can be used to zip a materials
    """
    pass

class MaterialZipView(MultipleMaterialZipResponseMixin, BaseListView):
    """
        generate zip archive from queryset.
    """
    pass
