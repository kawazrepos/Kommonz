from auth.models import KommonzUser
from django.forms.models import ModelForm


class UserUpdateForm(ModelForm):

    class Meta:
        model = KommonzUser
        fields = ('nickname', 'icon', 'sex', 'birthday', 'place', 'url', 'email', 'email_notification', 'profile',)