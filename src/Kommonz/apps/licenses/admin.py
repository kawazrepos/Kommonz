from django.contrib import admin
from models import License, CodeLicense, CCLicense


class LicenceAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
admin.site.register(License, LicenceAdmin)

class CodeLicenseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
admin.site.register(CodeLicense, CodeLicenseAdmin)

class CCLicenseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
admin.site.register(CCLicense, CCLicenseAdmin)