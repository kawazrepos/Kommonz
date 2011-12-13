# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/forms.py
# created by giginet on 2011/10/14
#
from django import forms
from models import Material, MaterialFile
from django.utils.translation import ugettext as _

class MaterialForm(forms.ModelForm):
    _file = forms.IntegerField(widget=forms.HiddenInput())
    
    class Meta:
        model  = Material

class MaterialFileForm(forms.ModelForm):

    class Meta:
        model = MaterialFile

class MaterialUpdateForm(forms.ModelForm):
    """
    A Form Class for updateting Material.
    User can't update license and file of Material instance.
    """

    def __init__(self, **kwargs):
        self.material = kwargs.pop('material', None)
        super(MaterialUpdateForm, self).__init__(**kwargs)
        self.fields.get('file').initial = self.material.file

    file = forms.FileField(_("File"))

    class Meta:
        model = Material
        exclude = ('license', '_file')
