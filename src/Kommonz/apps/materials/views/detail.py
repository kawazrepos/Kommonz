# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/views/detail.py
# created by giginet on 2011/11/15
#
from django.views.generic import DetailView
from ..models import Material

class MaterialDetailView(DetailView):
    model = Material
