# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
import shutil
import commands
import tempfile
from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from utils.ffmpeg import get_playtime
from ..models import Material
from ..managers import MaterialManager

class Movie(Material):
    """
        Model for Movie material.
    """
    
    play_time = models.PositiveSmallIntegerField(_('Play Time'), editable=False, default=0)

    objects = MaterialManager()
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Movie')
        verbose_name_plural = _('Movies')

    @property
    def media(self):
        if self.extension == 'mp4':
            return 'm4v'
        return self.extension

    def save(self, *args, **kwargs):
        if not self._thumbnail:
            path = self._get_thumbnail_path(os.path.basename(self.file.path))
            thumbnail_path = "%s.png" % os.path.splitext(path)[0]
            created = self._create_thumbnail(path=os.path.join(settings.MEDIA_ROOT, thumbnail_path))
            if created:
                self._thumbnail = thumbnail_path
                signals.post_save.connect(self._thumbnail.field._create_thumbnails, sender=Movie)
            if not self.play_time:
                self.play_time = int(get_playtime(self.file.path))
        super(Movie, self).save(*args, **kwargs)

    def _create_thumbnail(self, path, second=30):
        """
        Create thumbnail from movie file.
        Returns thumbnail creation succeed or failed.
        """
        thumbnail_dir = os.path.dirname(path)
        if not os.path.exists(thumbnail_dir):
            os.makedirs(thumbnail_dir)
        f = open(self.file.path, 'rb')
        tmp = tempfile.NamedTemporaryFile(suffix=".%s" % self.extension, delete=False)
        tmp.write(f.read())
        tmp.close()
        f.close()
        thumbnail = tempfile.NamedTemporaryFile()
        thumbnail.close()
        ffmpeg = """ffmpeg -ss %(sec)s -vframes 1 -i "%(movie)s" -f image2 "%(output)s" """
        kwargs = {
                "sec" : second,
                "movie" : tmp.name,
                "width" : 288,
                "height" : 288,
                "output" : thumbnail.name
        }
        for sec in xrange(0, second, 10):
            kwargs['sec'] = second - sec
            try:
                commands.getstatusoutput(ffmpeg % kwargs)[0]
            except:
                return False
            if os.path.exists(thumbnail.name):
                shutil.move(thumbnail.name, path)
                return True
            return False
