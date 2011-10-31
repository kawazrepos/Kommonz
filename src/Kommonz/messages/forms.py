from auth.models import KommonzUser
from django import forms
from django.forms.models import ModelForm
from models import Message


class MessageCreateForm(ModelForm):
    users_to = forms.ModelMultipleChoiceField(queryset=KommonzUser.objects.all())
    
    class Meta:
        model = Message
        fields = ('label', 'users_to', 'body',)


class MaterialMessageCreateForm(ModelForm):

    class Meta:
        model = Message
        fields = ('label', 'body',)


class ReplyMessageCreateForm(ModelForm):

    class Meta:
        model = Message
        fields = ('label', 'body',)

class MessageDeleteForm(ModelForm):
   
    class Meta:
        model = Message
        fields = ()
