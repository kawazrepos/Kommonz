# -*- coding: utf-8 -*-
#    
#    Kommonz.materials.models.base
#    created by giginet on 2011/10/02
#
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import os

class MaterialManager(models.Manager):
    pass

class Material(models.Manager):
    u"""abstract model of whole materials."""
    
    def get_file_path(self, filename):
        return filename
    
    # required
    label       = models.CharField(_('label'), max_length=128)
    description = models.TextField(_('description'))
    file        = models.FilePathField(_('file'), path=get_file_path)
    
    # auto add
    created_at  = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at  = models.DateTimeField(_('Updated At'), auto_now=True)
    author      = models.ForeignKey(User, verbose_name=_('author'), editable=False)
    pv          = models.PositiveIntegerField(_('Page View'), default=0, editable=False)
    download    = models.PositiveIntegerField(_('Download Count'), default=0, editable=False)
    ip          = models.IPAddressField(_('IP Address'), editable=False)
    
    object      = MaterialManager()
    
    class Meta:
        ordering            = '-created_at'
        verbose_name        = _('Material')
        verbose_name_plural = _('Materials')
        
    @models.permalink
    def get_absolute_url(self):
        return ""