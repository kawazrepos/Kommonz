# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/lists/forms.py
# created by giginet on 2011/12/02
#
from django import forms
from models import ORDER_STATES

class ListOrderForm(forms.Form):
    order = forms.ChoiceField(choices=ORDER_STATES)
