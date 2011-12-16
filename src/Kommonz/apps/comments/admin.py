from django.contrib import admin
from apps.comments.models import MaterialComment


class MaterialCommentAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(MaterialComment, MaterialCommentAdmin)