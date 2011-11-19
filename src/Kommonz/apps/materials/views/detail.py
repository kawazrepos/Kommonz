# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/views/detail.py
# created by giginet on 2011/11/15
#
from django.views.generic import DetailView
from ..models import Material

class MaterialDetailView(DetailView):
    model = Material
    template_name = "materials/material_detail.html"

    def get_object(self, queryset=None):
        instance = super(MaterialDetailView, self).get_object(queryset)
        return instance.model.objects.get(pk=instance.pk)
