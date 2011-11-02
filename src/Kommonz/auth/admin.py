from auth.models import UserProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'

class KommonzUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    list_display = ('nickname', 'username', 'sex', 'birthday', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'sex',)
admin.site.register(UserProfile)