# -*- coding: utf-8 -*-
#
# src/Kommonz/thumbnailfield/models.py
# created by giginet on 2011/11/06
#
import os
import shutil
from django.db.models.fields.files import ImageField
from django.db.models import signals
from django.conf import settings
from widgets import DelAdminFileWidget
from forms import ThumbnailFormField
from exceptions import DuplicatePatterNameException

THUMBNAILFIELD_THUMBNAIL_DIRNAME = getattr(settings, 'THUMBNAILFIELD_THUMBNAIL_DIR_NAME', '')
THUMBNAILFIELD_THUMBNAIL_FILENAME = getattr(settings, 'THUMBNAILFIELD_THUMBNAIL_FILENAME', None)

class ThumbnailField(ImageField):
    def __init__(self, *args, **kwargs):
        thumbnail_size_patterns = kwargs.pop('thumbnail_size_patterns', ())
        self.thumbnail_dirname = kwargs.pop('thumbnail_dirname', THUMBNAILFIELD_THUMBNAIL_DIRNAME)
        self.thumbnail_size_patterns = self._convert_patterns_dict(thumbnail_size_patterns)
        super(ThumbnailField, self).__init__(*args, **kwargs) 

    def formfield(self, **kwargs):
        """
        Specify form field and widget to be used on the forms
        """
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
        """
        Overwrite get_db_prep_save to allow saving nothing to the database
        if image has been deleted
        """
        if value:
            return super(ImageField, self).get_db_prep_save(value)
        else:
            return u''

    def contribute_to_class(self, cls, name):
        """
        Call methods for generating all operations on specified signals
        """
        super(ImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._create_thumbnails, sender=cls)
        signals.post_init.connect(self._set_thumbnails, sender=cls)

    def _get_filename(self):
        filename = THUMBNAILFIELD_THUMBNAIL_FILENAME
        if not filename:
            return self.name
        return filename

    def _create_thumbnails(self, sender, instance, created, **kwargs):
        """
        Renames the image, and calls methods to resize and create the thumbnail
        """
        filename = self._get_filename()
        file = getattr(instance, self.name, None)
        if not file: return
        fullpath = getattr(file, 'path', None)
        ext = os.path.splitext(fullpath)[1].lower().replace('jpg', 'jpeg')
        dst = self.generate_filename(instance, '%s_%s%s' % (filename, instance._get_pk_val(), ext))
        dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)
        dst_dir = os.path.dirname(dst_fullpath)
        thumbnail_dir = self._get_thumbnail_dir(dst_fullpath)
        if created or not os.path.abspath(fullpath) == os.path.abspath(dst_fullpath):
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            if not os.path.exists(dst_fullpath):
                shutil.copy(fullpath, dst_fullpath)
            if not os.path.exists(thumbnail_dir):
                os.mkdir(thumbnail_dir)
            self._create_thumbnail(dst_fullpath, thumbnail_dir, self.thumbnail_size_patterns)
            setattr(instance, self.attname, dst)
            instance.save()

    def _get_thumbnail_dir(self, fullpath):
        dirpath = os.path.dirname(fullpath)
        return os.path.join(dirpath, self.thumbnail_dirname)

    def _set_thumbnails(self, instance=None, **kwargs):
        """
        Creates a "thumbnail" object as attribute of the ImageField instance
        Thumbnail attribute will be of the same class of original image, so
        "path", "url"... properties can be used
        """
        file = getattr(instance, self.name, None)
        if file:
            dirpath, filename = os.path.split(file.name)
            thumbnail_dir = self._get_thumbnail_dir(file.name)
            for pattern_name, pattern_size in self.thumbnail_size_patterns.iteritems():
                if hasattr(getattr(instance, self.name), pattern_name):
                    raise DuplicatePatterNameException(pattern_name)
                thumbnail_filename = self._get_thumbnail_filename(filename, pattern_name)
                thumbnail = self.attr_class(instance, self, os.path.join(thumbnail_dir, thumbnail_filename))
                setattr(getattr(instance, self.name), pattern_name, thumbnail)

    def _get_thumbnail_filename(self, filename, pattern_name):
        """
        Returns the thumbnail name associated to the standard image filename
            * Example: /var/www/myproject/media/img/picture_1.jpeg
                will return /var/www/myproject/media/img/picture_1.thumbnail.jpeg
        """
        splitted_filename = list(os.path.splitext(filename))
        splitted_filename.insert(1, '.%s' % pattern_name)
        return ''.join(splitted_filename)

    def _convert_patterns_dict(self, thumbnail_size_patterns):
        PARAMS_SIZE = ('width', 'height', 'force')
        patterns_dict = {}
        for pattern_name, thumbnail_size in thumbnail_size_patterns.iteritems():
            patterns_dict[pattern_name] = dict(map(None, PARAMS_SIZE, thumbnail_size))
        return patterns_dict

    def _create_thumbnail(self, src, thumbnail_dirname, patterns):
        """
        Create resized thumbnail of 'src' into 'thumbnail_dirname' via 'patterns'.
        """
        for pattern_name, pattern_size in patterns.iteritems():
            filename = os.path.basename(src)
            thumbnail_filename = self._get_thumbnail_filename(filename, pattern_name)
            thumbnail_path = os.path.join(thumbnail_dirname, thumbnail_filename)
            if not os.path.exists(thumbnail_dirname):
                os.makedirs(thumbnail_dirname)
            if os.path.exists(src):
                shutil.copy(src, thumbnail_path)
                self._resize_image(thumbnail_path, pattern_size)

    def _resize_image(self, filepath, size):
        """
        Resizes the image to specified width, height and force option
            - filename: full path of image to resize
            - size: dictionary containing:
                - width: new width
                - height: new height
                - force: if True, image will be cropped to fit the exact size,
                    if False, it will have the bigger size that fits the specified
                    size, but without cropping, so it could be smaller on width or height
        """
        try:
            from PIL import Image, ImageOps
        except ImportError:
            import Image
            import ImageOps
        WIDTH, HEIGHT = 0, 1
        img = Image.open(filepath)
        if img.size[WIDTH] > size['width'] or img.size[HEIGHT] > size['height']:
            if size['force']:
                img = ImageOps.fit(img, (size['width'], size['height']), Image.ANTIALIAS)
            else:
                img.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
            try:
                img.save(filepath, optimize=1)
            except IOError:
                img.save(filepath)
