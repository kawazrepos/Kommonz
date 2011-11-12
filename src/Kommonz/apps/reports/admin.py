from django.contrib import admin
from models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display    = ('material', '__unicode__', 'created_at', 'author',)
    ordering        = ['created_at']

admin.site.register(Report, ReportAdmin)