from Kommonz.massages.models import Massage
from django import forms

class MaterialForm(forms.ModelForm):
    class Meta:
        model  = Massage
        fields = ('subject', 'user_to', )