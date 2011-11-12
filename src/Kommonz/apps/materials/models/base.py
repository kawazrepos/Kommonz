# -*- coding: utf-8 -*-
#    
#    Kommonz.apps.materials.models.base
#    created by giginet on 2011/10/02
#
import os
import mimetypes
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _
from object_permission.mediators import ObjectPermissionMediator as Mediator
from qwert.middleware.threadlocals import request as get_request
from apps.categories.models import Category
from fields.ccfield.models import CreativeCommonsField
from fields.thumbnailfield.models import ThumbnailField
from ..managers import MaterialManager

class MaterialFile(models.Model):
    u"""
        model for file
    """
    
    def _get_file_path(self, filename):
        request = get_request()
        if not request:
            user = User.objects.get(pk=1)
        else:
            user = request.user
        path = u'storage/materials/%s/' % user.username
        return os.path.join(path, filename)
    
    file       = models.FileField(_('File'), upload_to=_get_file_path)
    
    class Meta:
        app_label           = 'materials'
        ordering            = ('-material__pk',)
        verbose_name        = _('MaterialFile')
        verbose_name_plural = _('MaterialFiles')

    def __unicode__(self):
        return self.file.name
    
    def save(self, *args, **kwargs):
        return super(MaterialFile, self).save(*args, **kwargs)

    @property
    def extension(self):
      return os.path.splitext(self.file.name)[1][1:]


class Material(models.Model):
    u"""
        abstract model of whole materials.
    """
    
    def _get_thumbnail_path(self, filename):
        path = u'storage/materials/%s/thumbnails/' % self.author.username
        return os.path.join(path, filename)
    
    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (96, 96, False),
        'middle':   (48, 48, False),
        'small':    (24, 24, False),
    }
    
    # required
    label       = models.CharField(_('Label'), max_length=128, null=False, blank=True)
    category    = models.ForeignKey(Category, verbose_name=_('Category'), related_name="materials")
    
    # not required 
    description = models.TextField(_('Description'), blank=False, null=True)
    thumbnail   = ThumbnailField(_('Thumbnail'), upload_to=_get_thumbnail_path, thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS, null=True, blank=True)
    _file       = models.OneToOneField(MaterialFile, verbose_name=('Material'), related_name='material')
    
    # auto add
    created_at  = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at  = models.DateTimeField(_('Updated At'), auto_now=True)
    author      = models.ForeignKey(User, verbose_name=_('author'), editable=False, related_name="materials")
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
        return '%s(%s)' % (self.label, self.file.name)
    
    def clean(self):
        return super(Material, self).clean()
            
    @models.permalink
    def get_absolute_url(self):
        return ('materials_material_detail', (), {'pk': self.pk})
    
    def get_thumbnail_url(self):
        return self.file.path

    @property
    def file(self):
        return self._file.file
    
    @property
    def mimetype(self):
        try:
            mimetypes.init()
            type = mimetypes.guess_type(self.file.name)[0]
        except:
            type = None
        return type
    
    @property
    def filetype_model(self):
        from ..utils.filetypes import get_file_model
        return get_file_model(self.file.name)
    
    @property
    def encoding(self):
        try:
            mimetypes.init()
            encoding = mimetypes.guess_type(self.file.name)[1]
        except:
            encoding = None
        return encoding
    
    @property
    def extension(self):
      return os.path.splitext(self.file.name)[1][1:]
    
    def save(self, *args, **kwargs):
        from ..utils.filetypes import get_file_model
        cls = get_file_model(self.label)
        if not isinstance(self, cls):
            extended = cls(pk=self.pk)
            extended.__dict__.update(self.__dict__)
            extended.save()
        request = get_request()
        if not self.label:
            self.label = self.file.name
        if request and request.user.is_authenticated():
            self.author = request.user
            self.ip = request.META['REMOTE_ADDR']
        else:
            self.author = User.objects.get(pk=1)
            self.ip = "0.0.0.0"
        return super(Material, self).save(*args, **kwargs)
    
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author)
        # ToDo collaborators
        # map(lambda user: mediator.editor(self, user), self.collaborators)
        
        
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

    commons       = CreativeCommonsField(_('Creative Commons'))
    material      = models.OneToOneField('Material', verbose_name=_('Creative Commons'), parent_link=True)
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Creative Commons')
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self._get_commons_description()
    
    def _get_commons_description(self):
        nc, nd, sa = self.commons.noncommerical, self.commons.no_derivative, self.commons.share_alike
        if not nd:
            return 'CC BY' if not nc else 'CC BY-NC'
        elif not nd and sa:
            return 'CC BY-SA' if not nc else 'CC-BY-NC-SA'
        elif nd:
            return 'CC BY-ND' if not nc else 'CC BY-NC-ND'
        
    def clean(self):
        if self.commons.no_derivative and self.commons.share_alike:
            raise ValidationError(_('''can not set 'Share Alike' and 'Not Derivative Works' together.'''))
        return super(CreativeCommons, self).clean()
    
