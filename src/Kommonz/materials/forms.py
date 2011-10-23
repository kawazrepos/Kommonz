# -*- coding: utf-8 -*-
#
# src/Kommonz/materials/forms.py
# created by giginet on 2011/10/14
#
from django import forms
from models.base import MaterialFile

class MaterialForm(forms.ModelForm):
    class Meta:
        model  = MaterialFile
        fields = ('file', )
