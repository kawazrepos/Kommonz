from django.contrib import admin
from models import UserProfile, UserOption

__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'description', 'icon', 'sex', 'birthday', 'place', 'url',)


class UserOptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notification',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserOption, UserOptionAdmin)