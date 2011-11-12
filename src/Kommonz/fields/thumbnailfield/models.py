# -*- coding: utf-8 -*-
#
# src/Kommonz/thumbnailfield/models.py
# created by giginet on 2011/11/06
#
import os, shutil
from django.db.models.fields.files import ImageField
from django.db.models import signals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from widgets import DelAdminFileWidget
from forms import ThumbnailFormField
from exceptions import DuplicatePatterNameException

class ThumbnailField(ImageField):
    def __init__(self, size=None, *args, **kwargs):
        params_size = ('width', 'height', 'force')
        self.size = dict(map(None, params_size, size)) if size else None
        thumbnail_size_patterns = kwargs.pop('thumbnail_size_patterns', ())
        self.pattern_names = [pattern_name for pattern_name, thumbnail_size in thumbnail_size_patterns.iteritems()]
        for pattern_name, thumbnail_size in thumbnail_size_patterns.iteritems():
            setattr(self, "%s_size" % pattern_name, dict(map(None, params_size, thumbnail_size)))
        super(ThumbnailField, self).__init__(*args, **kwargs) 

    @staticmethod
    def _get_thumbnail_filename(filename, pattern_name):
        '''
        Returns the thumbnail name associated to the standard image filename
            * Example: /var/www/myproject/media/img/picture_1.jpeg
                will return /var/www/myproject/media/img/picture_1.thumbnail.jpeg
        '''
        splitted_filename = list(os.path.splitext(filename))
        splitted_filename.insert(1, '.%s' % pattern_name)
        return ''.join(splitted_filename)
    
    @staticmethod
    def _resize_image(filename, size):
        '''
        Resizes the image to specified width, height and force option
            - filename: full path of image to resize
            - size: dictionary containing:
                - width: new width
                - height: new height
                - force: if True, image will be cropped to fit the exact size,
                    if False, it will have the bigger size that fits the specified
                    size, but without cropping, so it could be smaller on width or height
        '''
        WIDTH, HEIGHT = 0, 1
        try:
            from PIL import Image, ImageOps
        except ImportError:
            import Image
            import ImageOps
            
        img = Image.open(filename)
        if img.size[WIDTH] > size['width'] or img.size[HEIGHT] > size['height']:
            if size['force']:
                img = ImageOps.fit(img, (size['width'], size['height']), Image.ANTIALIAS)
            else:
                img.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
            try:
                img.save(filename, optimize=1)
            except IOError:
                img.save(filename)

    def _rename_resize_image(self, sender, instance, created, **kwargs):
        '''
        Renames the image, and calls methods to resize and create the thumbnail
        '''
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            ext = os.path.splitext(filename)[1].lower().replace('jpg', 'jpeg')
            dst = self.generate_filename(instance, '%s_%s%s' % (self.name, instance._get_pk_val(), ext))
            dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)
            if created or os.path.abspath(filename) != os.path.abspath(dst_fullpath):
                if 'fixtures' in filename:
                    if not os.path.exists(os.path.dirname(dst_fullpath)):
                        os.makedirs(os.path.dirname(dst_fullpath))
                    shutil.copyfile(filename, dst_fullpath)
                elif os.path.exists(filename):
                    os.rename(filename, dst_fullpath)
                if self.size:
                    self._resize_image(dst_fullpath, self.size)
                for pattern_name in self.pattern_names:
                    thumbnail_filename = self._get_thumbnail_filename(dst_fullpath, pattern_name)
                    shutil.copyfile(dst_fullpath, thumbnail_filename)
                    self._resize_image(thumbnail_filename, getattr(self, "%s_size" % pattern_name))
                setattr(instance, self.attname, dst)
                instance.save()

    def _set_thumbnails(self, instance=None, **kwargs):
        '''
        Creates a "thumbnail" object as attribute of the ImageField instance
        Thumbnail attribute will be of the same class of original image, so
        "path", "url"... properties can be used
        '''
        if getattr(instance, self.name):
            filename = self.generate_filename(instance, os.path.basename(getattr(instance, self.name).path))
            for pattern_name in self.pattern_names:
                if hasattr(getattr(instance, self.name), pattern_name):
                    raise DuplicatePatterNameException(pattern_name)
                thumbnail_filename = self._get_thumbnail_filename(filename, pattern_name)
                thumbnail_type = self.attr_class(instance, self, thumbnail_filename)
                setattr(getattr(instance, self.name), pattern_name, thumbnail_type)

    def _get_thumbnail_file(self, instance, pattern_name):
        if getattr(instance, self.name):
            try:
                from PIL import Image, ImageOps
            except ImportError:
                import Image
                import ImageOps
            filename = self.generate_filename(instance, os.path.basename(getattr(instance, self.name).path))
            thumbnail_filename = self._get_thumbnail_filename(filename, pattern_name)
            return Image.open(thumbnail_filename)
        return None

    def formfield(self, **kwargs):
        '''
        Specify form field and widget to be used on the forms
        '''
        kwargs['widget'] = DelAdminFileWidget
        kwargs['form_class'] = ThumbnailFormField
        return super(ImageField, self).formfield(**kwargs)

    def save_form_data(self, instance, data):
        '''
            Overwrite save_form_data to delete images if "delete" checkbox
            is selected
        '''
        if data == '__deleted__':
            filename = getattr(instance, self.name).path
            if os.path.exists(filename):
                os.remove(filename)
            for pattern_name in self.pattern_names:
                thumbnail_filename = self._get_thumbnail_filename(filename, pattern_name)
                if os.path.exists(thumbnail_filename):
                    os.remove(thumbnail_filename)
            setattr(instance, self.name, None)
        else:
            super(ImageField, self).save_form_data(instance, data)

    def get_db_prep_save(self, value):
        '''
            Overwrite get_db_prep_save to allow saving nothing to the database
            if image has been deleted
        '''
        if value:
            return super(ImageField, self).get_db_prep_save(value)
        else:
            return u''

    def contribute_to_class(self, cls, name):
        '''
        Call methods for generating all operations on specified signals
        '''
        super(ImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._rename_resize_image, sender=cls)
        signals.post_init.connect(self._set_thumbnails, sender=cls)

