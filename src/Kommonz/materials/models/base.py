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
    u"""
        abstract model of whole materials.
    """
    
    def get_file_path(self, filename):
        return filename
    
    # required
    label       = models.CharField(_('Label'), max_length=128)
    description = models.TextField(_('Description'))
    file        = models.FilePathField(_('File'), path=get_file_path)
    
    # auto add
    created_at  = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at  = models.DateTimeField(_('Updated At'), auto_now=True)
    author      = models.ForeignKey(User, verbose_name=_('author'), editable=False, related_name="materials")
    pv          = models.PositiveIntegerField(_('Page View'), default=0, editable=False)
    download    = models.PositiveIntegerField(_('Download Count'), default=0, editable=False)
    ip          = models.IPAddressField(_('IP Address'), editable=False)
    license     = models.ForeignKey('License', verbose_name=_('License'))
    
    objects     = MaterialManager()
    
    class Meta:
        abstract            = True
        ordering            = ('-created_at',)
        verbose_name        = _('Material')
        verbose_name_plural = _('Materials')
        
    @models.permalink
    def get_absolute_url(self):
        return ""

class Kero(object):
    u"""
        Kero is a rating system for Materials.
    """
    
    def get_file_path(self, filename):
        return filename
    
    label       = models.CharField(_('Label'), max_length=32)
    description = models.TextField(_('Description'))
    icon        = models.FilePathField(_('Icon'), path=get_file_path)
    materials   = models.ManyToManyField(Material, related_name='keros', verbose_name=_('materials'))
    
    class Meta:
        ordering            = ('pk',)
        verbose_name        = _('KERO')
        verbose_name_plural = verbose_name

class License(models.Model):
    u"""
        License
    """
    
    label        = models.CharField(_('Label'), max_length=32)
    description  = models.TextField(_('Description'))

    class Meta(License.Meta):
        verbose_name        = _('License')
        verbose_name_plural = _('Licenses') 

class CreativeCommons(object):
    u"""
        CreativeCommons http://en.wikipedia.org/wiki/Creative_Commons
    """

    noncommerical = models.BooleanField(_('Noncommerical'), default=False)
    no_derivative = models.BooleanField(_('No Derivative Works'), default=False)
    share_alike   = models.BooleanField(_('Share Alike'), default=False)
    material      = models.OneToOneField(Material, verbose_name=_('Creative Commons'), related_name='commons')
    
    class Meta(object):
        verbose_name        = _('CreaticeCommons')
        verbose_name_plural = verbose_name