from django.contrib import admin
from models import Kero


class KeroAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
admin.site.register(Kero, KeroAdmin)

