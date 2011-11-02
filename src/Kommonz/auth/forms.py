
from django.contrib.auth.models import User
from django.forms.models import ModelForm


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email',)