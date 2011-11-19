from django.contrib import admin
from models import License, CreativeCommons


class LisenceAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(License, LisenceAdmin)

class CreativeCommonsAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(CreativeCommons, CreativeCommonsAdmin)