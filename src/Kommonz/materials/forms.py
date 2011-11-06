# -*- coding: utf-8 -*-
#
# src/Kommonz/materials/forms.py
# created by giginet on 2011/10/14
#
from django import forms
from models.base import Material, MaterialFile

class MaterialForm(forms.ModelForm):
    _file = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model  = Material

class MaterialFileForm(forms.ModelForm):

    class Meta:
        model = MaterialFile
