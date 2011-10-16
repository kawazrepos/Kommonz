from django.contrib import admin
from Kommonz.massages.models import Massage

class MassageAdmin(admin.ModelAdmin):
    date_hierarchy  = 'sent_at'
    list_display    = ('__unicode__', 'user_from', 'user_to', 'is_already_read', 'sent_at',)
    
admin.site.register(Massage, MassageAdmin)