from django.contrib import admin
from massages.models import Massage


class MassageAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'user_from', 'user_to', 'read', 'created_at',)
    
admin.site.register(Massage, MassageAdmin)