from django.contrib.auth.models import User
from django.forms.models import ModelForm
from models import UserProfile, UserOption


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        
        
class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nickname', 'description', '_avatar', 'sex', 'birthday', 'place', 'url',)        
        
class UserOptionUpdateForm(ModelForm):
    class Meta:
        model = UserOption
        fields = ('email_notification',)
