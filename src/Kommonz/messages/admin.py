from django.contrib import admin
from messages.models import Message


class MessageAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'user_from', 'user_to', 'read', 'created_at',)
    
admin.site.register(Message, MessageAdmin)