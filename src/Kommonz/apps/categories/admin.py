from django.contrib import admin
from apps.categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__', 'parent',)
    ordering        = ['id']

admin.site.register(Category, CategoryAdmin)