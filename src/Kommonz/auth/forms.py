from auth.models import UserProfile
from django.contrib.auth.models import User
from django.forms.models import ModelForm


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
        
        
class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nickname', 'profile', 'icon', 'sex', 'birthday', 'place', 'url')
        