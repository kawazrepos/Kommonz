# -*- coding: utf-8 -*-
#    
#    Kommonz.apps.materials.models.base
#    created by giginet on 2011/10/02
#
import os
import mimetypes
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext as _
from qwert.middleware.threadlocals import request as get_request
from apps.categories.models import Category

from fields.thumbnailfield.fields import ThumbnailField
from managers import MaterialManager

MATERIAL_FILE_PATH = os.path.join('storage', 'materials')
DEFAULT_THUMBNAIL_PATH = os.path.join('image', 'default', 'material', '%s.png')

class MaterialFile(models.Model):
    """
    A Model for material raw file.
    """
    def _get_file_path(self, filename):
        request = get_request()
        if not request:
            user = User.objects.get(pk=1)
        else:
            user = request.user
        path = os.path.join(MATERIAL_FILE_PATH, user.username, filename)
        path = default_storage.get_available_name(path) # dirname will not duplicate.
        return os.path.join(path, filename)
    
    file   = models.FileField(_('File'), upload_to=_get_file_path)
    author = models.ForeignKey(User, verbose_name=_('author'), editable=False, related_name="materialfiles")
    
    class Meta:
        app_label           = 'materials'
        ordering            = ('-material__pk',)
        verbose_name        = _('MaterialFile')
        verbose_name_plural = _('MaterialFiles')

    def save(self, *args, **kwargs):
        request = get_request()
        if request and request.user.is_authenticated():
            self.author = request.user
        else:
            self.author = User.objects.get(pk=1)
        super(MaterialFile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.file.name

    @property
    def extension(self):
      return os.path.splitext(self.file.name)[1][1:]

class Material(models.Model):
    """
    A model for all materials.
    """
   
    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (144, 144, False),
        'middle':   (96, 96, False),
        'small':    (27, 27, False),
    }

    def _get_thumbnail_path(self, filename):
        path = os.path.dirname(self.file.name)
        name, ext = os.path.splitext(filename)
        thumbnail_name = default_storage.get_available_name('thumbnail%s' % ext)
        return os.path.join(path, 'thumbnails', thumbnail_name)
    
    # required
    label       = models.CharField(_('Label'), max_length=128, null=False, blank=False)
    _file       = models.OneToOneField(MaterialFile, verbose_name=('Material'), related_name='material')

    # not required 
    description = models.TextField(_('Description'), blank=True, null=True)
    category    = models.ForeignKey(Category, verbose_name=_('Category'), related_name='materials', blank=True, null=True)
    
    # auto add
    created_at  = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at  = models.DateTimeField(_('Updated At'), auto_now=True)
    author      = models.ForeignKey(User, verbose_name=_('author'), editable=False, related_name="materials")
    pv          = models.PositiveIntegerField(_('Page View'), default=0, editable=False)
    download    = models.PositiveIntegerField(_('Download Count'), default=0, editable=False)
    ip          = models.IPAddressField(_('IP Address'), editable=False)
    _thumbnail   = ThumbnailField(_('Thumbnail'), upload_to=_get_thumbnail_path, thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS, null=True, blank=True)
    
    objects     = MaterialManager()
    
    class Meta:
        app_label           = 'materials'
        ordering            = ('-created_at',)
        verbose_name        = _('Material')
        verbose_name_plural = _('Materials')
        
    def __unicode__(self):
        return '%s(%s)' % (self.label, self.file.name)
    
    def clean(self):
        if not self.category:
            self.category = Category.objects.get_filetype_category(self.file.name)
        return super(Material, self).clean()
            
    @models.permalink
    def get_absolute_url(self):
        return ('materials_material_detail', (), {'pk': self.pk})

    def _get_default_thumbnail_path(self):
        return DEFAULT_THUMBNAIL_PATH % self.filetype

    @property
    def thumbnail(self):
        """
        Returns thumbnail file to display.
        """
        return ThumbnailFile(self, self._thumbnail.field)
    
    @property
    def file(self):
        """
        Alias for MaterialFile.file
        """
        return self._file.file
    
    @property
    def mimetype(self):
        """
        Returns mimetype of own file
        Example : 'audio/wav'.
        """
        try:
            mimetypes.init()
            type = mimetypes.guess_type(self.file.name)[0]
        except:
            type = None
        return type

    @property
    def filetype(self):
        """
        Returns file type name like 
        Example : 'audio'
        """
        from utils.filetypes import guess
        return guess(self.file.name)

    @property
    def size(self):
        """
        Returns filesize(byte).
        """
        try:
            return self.file.size
        except:
            return 0
    
    @property
    def model(self):
        """
        Returns it's model class.
        """
        from utils.filetypes import get_file_model
        return get_file_model(self.file.name)
    
    @property
    def extension(self):
        """
        Returns extension of own file.
        It may not be include '.' and casted to lower case.
        hoge.png #=> png
        hoge.MP3 #=> mp3
        """
        return os.path.splitext(self.file.name)[1][1:].lower()

    @property
    def filename(self):
        """
        Returns filename of own file.
        """
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        from utils.filetypes import get_file_model
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
        if not self.category:
            self.category = Category.objects.get_filetype_category(self.file.name)
        return super(Material, self).save(*args, **kwargs)
    
    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author)
        mediator.viewer(self, None)
        mediator.viewer(self, 'anonymous')
        
class Kero(models.Model):
    """
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

@receiver(pre_delete, sender=Material)
def delete_material_file(sender, instance, **kwargs):
    import shutil
    if os.path.exists(os.path.dirname(instance.file.path)):
        shutil.rmtree(os.path.dirname(instance.file.path))

class ThumbnailFile(ImageFieldFile):
    """
    Thumbnail Image class.
    """
    def __init__(self, instance, field):
        if instance._thumbnail:
            self.thumbnail = instance._thumbnail.name
        else:
            self.thumbnail = instance._get_default_thumbnail_path()
        super(ImageFieldFile, self).__init__(instance, field, self.thumbnail)
        for pattern_name, pattern_size in Material.THUMBNAIL_SIZE_PATTERNS.iteritems():
            path, ext = os.path.splitext(self.thumbnail)
            setattr(self, pattern_name, ImageFieldFile(instance, field, "%s.%s%s" % (path, pattern_name, ext)))
