# -*- coding: utf-8 -*-
#
# src/Kommonz/materials/forms.py
# created by giginet on 2011/10/14
#
from django import forms
from models.base import Material

class MaterialForm(forms.ModelForm):
    class Meta:
        model  = Material
        fields = ('file', )

class MaterialExtendForm(forms.ModelForm):
    
    class Meta:
        excludes = 'file'