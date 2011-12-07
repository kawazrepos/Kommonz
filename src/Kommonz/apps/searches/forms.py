# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/searches/forms.py
# created by giginet on 2011/12/06
#
from django import forms
from django.utils.translation import ugettext as _

from apps.categories.models import Category

SORTS = (
    ('pv',         _('PageView')),
    ('download',   _('Download')),
    ('created_at', _('Create Date')),
)

ORDERS = (
    ('d', _('Descending')),
    ('a', _('Ascending'))
)

THRESHOLDS = (
    ('o', _('Over')),
    ('b', _('Below'))
)

class SearchForm(forms.Form):
    """
    A Form on index page for searching material.
    """
    
    q        = forms.CharField(required=True)
    category = forms.ModelChoiceField(Category.objects.all())
    
    def __init__(self, query='', **kwargs):
        super(SearchForm, self).__init__(**kwargs)
        # self.q.initial = query

class ExtendSearchForm(SearchForm):
    """
    A Form on search result page.
    """
    sort       = forms.ChoiceField(choices=SORTS)
    order      = forms.ChoiceField(choices=ORDERS)
    download   = forms.IntegerField()
    thresholds = forms.ChoiceField(choices=THRESHOLDS)
