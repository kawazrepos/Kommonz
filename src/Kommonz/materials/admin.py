# -*- coding: utf-8 -*-
#    
#    Kommonz.materials.admin
#    created by giginet on 2011/10/02
#
from django.contrib import admin
from models.base import Material, Kero, License, CreativeCommons

class MaterialAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'author', 'license', 'created_at', 'ip', 'pv',)
    list_filter     = ('author', 'license',)
    search_fields   = ('label', 'description',)
admin.site.register(Material, MaterialAdmin)

class KeroAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Kero, KeroAdmin)

class LisenceAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(License, LisenceAdmin)

class CreativeCommonsAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(CreativeCommons, CreativeCommonsAdmin)