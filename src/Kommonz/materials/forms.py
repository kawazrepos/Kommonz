# -*- coding: utf-8 -*-
#
# src/Kommonz/materials/forms.py
# created by giginet on 2011/10/14
#
from django import forms
from models.base import MaterialData

class MaterialForm(forms.ModelForm):
    class Meta:
        model  = MaterialData
        fields = ('file', )