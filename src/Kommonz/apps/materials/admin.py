# -*- coding: utf-8 -*-
#    
#    Kommonz.apps.materials.admin
#    created by giginet on 2011/10/02
#
from django.contrib import admin
from models import MaterialFile, Material, Kero
from audios.models import Audio
from codes.models import Code
from images.models import Image
from movies.models import Movie
from packages.models import Package

# base models

class MaterialFileAdmin(admin.ModelAdmin):
    list_display    = ('pk', 'file', 'material', 'author',)
admin.site.register(MaterialFile, MaterialFileAdmin)

class MaterialAdmin(admin.ModelAdmin):
    date_hierarchy  = 'created_at'
    list_display    = ('__unicode__', 'author', 'created_at', '_file', 'ip', 'pv',)
    list_filter     = ('author',)
    search_fields   = ('label', 'description',)
admin.site.register(Material, MaterialAdmin)


# paticular models


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

class PackageAdmin(admin.ModelAdmin):
    list_display    = ('__unicode__',)
admin.site.register(Package, PackageAdmin)
