from django.contrib import admin
from models import List, ListInfo

class ListAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display   = ('__unicode__', 'author',  'pub_state', 'created_at', 'order')
    

class ListInfoAdmin(admin.ModelAdmin):
    pass
        
admin.site.register(List,ListAdmin)
admin.site.register(ListInfo,ListInfoAdmin)
