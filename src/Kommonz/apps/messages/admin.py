from django.contrib import admin
from models import Message


class MessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display   = ('__unicode__', 'user_from', 'user_to', 'read', 'pub_state', 'created_at',)
    
admin.site.register(Message, MessageAdmin)