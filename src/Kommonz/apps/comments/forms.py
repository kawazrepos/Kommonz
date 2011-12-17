from django import forms
from django.contrib.comments.forms import CommentDetailsForm
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _


class CommentForm(CommentDetailsForm):
    name          = forms.CharField(label=_("Name"), required=False, widget=HiddenInput)
    email         = forms.EmailField(label=_("Email address"), required=False, widget=HiddenInput)
    url           = forms.URLField(label=_("URL"), required=False, widget=HiddenInput)