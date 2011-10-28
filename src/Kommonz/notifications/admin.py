from django.contrib import admin
from notifications.models import Notification



class NotificationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display   = ('__unicode__', 'user_from', 'user_to', 'read', 'created_at',)
    
admin.site.register(Notification, NotificationAdmin)