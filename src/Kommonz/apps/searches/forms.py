# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/searches/forms.py
# created by tohhy on 2011/11/19
#
from apps.categories.models import Category
from django import forms


class SearchIndexForm(forms.Form):
    keyword = forms.CharField(max_length=500)
    category = forms.ChoiceField()
    
def get_category_choices():
    categories = list()
    for category in Category.objects.all():
        categories.append((category.label, category))
    return categories
_form = SearchIndexForm()
_form.fields['category'].choices = get_category_choices()
    
#class SearchImageForm(forms.Form):
#    
#    
#class SearchAudioForm(forms.Form):
    

