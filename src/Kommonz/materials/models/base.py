# -*- coding: utf-8 -*-
#    
#    Kommonz.materials.models.base
#    created by giginet on 2011/10/02
#
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import os

class MaterialManager(models.Manager):
    pass

class Material(models.Model):
    u"""
        abstract model of whole materials.
    """
    
    def _get_file_path(self, filename):
        return filename
    
    # required
    label       = models.CharField(_('Label'), max_length=128)
    description = models.TextField(_('Description'))
    file        = models.FileField(_('File'), upload_to=_get_file_path)
    
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
        ordering            = ('-created_at',)
        verbose_name        = _('Material')
        verbose_name_plural = _('Materials')
        
    def __unicode__(self):
        return self.label    
    
    @models.permalink
    def get_absolute_url(self):
        return ""

class Kero(models.Model):
    u"""
        Kero is a rating system for Materials.
    """
    
    def _get_file_path(self, filename):
        return filename
    
    label       = models.CharField(_('Label'), max_length=32)
    description = models.TextField(_('Description'))
    icon        = models.FileField(_('Icon'), upload_to=_get_file_path)
    materials   = models.ManyToManyField('Material', related_name='keros', verbose_name=_('materials'))
    
    class Meta:
        verbose_name        = _('KERO')
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.label

class License(models.Model):
    u"""
        License
    """
    
    label        = models.CharField(_('Label'), max_length=32)
    description  = models.TextField(_('Description'))

    class Meta:
        verbose_name        = _('License')
        verbose_name_plural = _('Licenses')
        
    def __unicode__(self):
        return self.label 

class CreativeCommons(models.Model):
    u"""
        CreativeCommons http://en.wikipedia.org/wiki/Creative_Commons
    """

    noncommerical = models.BooleanField(_('Noncommerical'), default=False)
    no_derivative = models.BooleanField(_('No Derivative Works'), default=False)
    share_alike   = models.BooleanField(_('Share Alike'), default=False)
    material      = models.OneToOneField('Material', verbose_name=_('Creative Commons'), parent_link=True)
    
    class Meta:
        verbose_name        = _('Creative Commons')
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self._get_commons_description()
    
    def _get_commons_description(self):
        nc, nd, sa = self.noncommerical, self.no_derivative, self.share_alike
        if not nd:
            return 'CC BY' if not nc else 'CC BY-NC'
        elif not nd and sa:
            return 'CC BY-SA' if not nc else 'CC-BY-NC-SA'
        elif nd:
            return 'CC BY-ND' if not nc else 'CC BY-NC-ND'
        
    def clean(self):
        if self.no_derivative and self.share_alike:
            raise ValidationError(_('''can not set 'Share Alike' and 'Not Derivative Works' together.'''))
        return super(CreativeCommons, self).clean()