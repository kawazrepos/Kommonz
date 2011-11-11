from django.contrib import admin
from models import Notification



class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display   = ('__unicode__', 'user_from', 'user_to', 'solved', 'created_at',)
    
admin.site.register(Notification, NotificationAdmin)