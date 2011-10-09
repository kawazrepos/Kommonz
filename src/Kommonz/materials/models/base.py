# -*- coding: utf-8 -*-
#    
#    Kommonz.materials.models.base
#    created by giginet on 2011/10/02
#
import os
import mimetypes
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from Kommonz.materials.managers import MaterialManager
from Kommonz.imagefield.fields import ImageField
from Kommonz.users.models import KommonzUser

class Material(models.Model):
    u"""
        abstract model of whole materials.
    """
    
    def _get_file_path(self, filename):
        path = u'storage/materials/%d/' % self.pk
        return os.path.join(path, filename)
    
    def _get_thumbnail_path(self, filename):
        path = u'storage/materials/%d/thumbnails/' % self.pk
        return os.path.join(path, filename)
    
    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (96, 96, False),
        'middle':   (48, 48, False),
        'small':    (24, 24, False),
    }
    
    # required
    label       = models.CharField(_('Label'), max_length=128)
    description = models.TextField(_('Description'))
    file        = models.FileField(_('File'), upload_to=_get_file_path)
    license     = models.ForeignKey(_('License'), verbose_name=_('License'))
    
    # not required 
    thumbnail   = ImageField(_('Thumbnail'), upload_to=_get_thumbnail_path, thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS)
    
    # auto add
    created_at  = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at  = models.DateTimeField(_('Updated At'), auto_now=True)
    author      = models.ForeignKey(KommonzUser, verbose_name=_('author'), editable=False, related_name="materials")
    pv          = models.PositiveIntegerField(_('Page View'), default=0, editable=False)
    download    = models.PositiveIntegerField(_('Download Count'), default=0, editable=False)
    ip          = models.IPAddressField(_('IP Address'), editable=False)
    
    objects     = MaterialManager()
    
    class Meta:
        app_label           = 'materials'
        ordering            = ('-created_at',)
        verbose_name        = _('Material')
        verbose_name_plural = _('Materials')
        
    def __unicode__(self):
        return self.label    
    
    @models.permalink
    def get_absolute_url(self):
        return ""
    
    def mimetype(self):
        try:
            mimetypes.init()
            type = mimetypes.guess_type(self.file.name)[0]
        except:
            type = None
        return type
    
    def encoding(self):
        try:
            mimetypes.init()
            encoding = mimetypes.guess_type(self.file.name)[1]
        except:
            encoding = None
        return encoding

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
        app_label           = 'materials'
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
        app_label           = 'materials'
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
        app_label           = 'materials'
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