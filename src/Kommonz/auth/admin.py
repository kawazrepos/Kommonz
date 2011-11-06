from django.contrib import admin
from auth.models import UserProfile, UserConfig

__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/09'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'description', 'icon', 'sex', 'birthday', 'place', 'url',)


class UserConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notification',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserConfig, UserConfigAdmin)