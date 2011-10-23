# -*- coding: utf-8 -*-
#    
#    Kommonz.materials.admin
#    created by giginet on 2011/10/02
#
from django.contrib import admin
from models.base import Material, Kero, License, CreativeCommons, Category
#from models.application import Application  保留
from models.archive import Archive
from models.audio import Audio
from models.code import Code
from models.image import Image
from models.movie import Movie


# base models

class MaterialAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'author', 'created_at', 'ip', 'pv',)
    list_filter     = ('author',)
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

class CategoryAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Category, CategoryAdmin)


# paticular models

class ArchiveAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Archive, ArchiveAdmin)

class AudioAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Audio, AudioAdmin)

class CodeAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Code, CodeAdmin)

class ImageAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Image, ImageAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Movie, MovieAdmin)
