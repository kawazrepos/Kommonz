# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
from cStringIO import StringIO
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from ..utils.syntaxes import SYNTAXES, guess_syntax
from ..models import Material
from ..managers import MaterialManager

class Code(Material):
    """
    Model for Source Code material.
    """
    def __init__(self, *args, **kwargs):
        super(Code, self).__init__(*args, **kwargs)
        thumbnail_field = [field for field in self._meta.fields if field.name == 'thumbnail']
        signals.post_init.connect(thumbnail_field[0]._set_thumbnails, sender=Code)
    
    syntax = models.CharField(_('Syntax'), max_length='32', choices=SYNTAXES)
    body   = models.TextField(_('Body'), editable=False)

    objects = MaterialManager()
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Code')
        verbose_name_plural = _('Codes')
    
    def clean(self):
        syntaxes = dict(SYNTAXES)
        if not self.syntax:
            self.syntax = self._guess_syntax()
        elif syntaxes.has_key(self.syntax):
            self.syntax = syntaxes[self.syntax]
        super(Code, self).clean()

    def save(self, *args, **kwargs):
        self.body = self._encode_body()
        path = self._get_thumbnail_path(os.path.basename(self.file.path))
        thumbnail_path = "%s.png" % os.path.splitext(path)[0]
        self._create_thumbnail(path=os.path.join(settings.MEDIA_ROOT, thumbnail_path))
        self.thumbnail = thumbnail_path
        thumbnail_field = [field for field in self._meta.fields if field.name == 'thumbnail']
        signals.post_save.connect(thumbnail_field[0]._create_thumbnails, sender=Code)
        signals.post_init.connect(thumbnail_field[0]._set_thumbnails, sender=Code)
        super(Code, self).save(*args, **kwargs)

    def _guess_syntax(self):
        """
        Guess a programming language from the filename
        """
        return guess_syntax(self.file.name)

    def _encode_body(self):
        """
        Read file to encode to utf8 and set into 'body' field.
        """
        from utils.encoding import to_utf8
        code = open(self.file.path, 'ra')
        body = to_utf8(code.read())
        code.close()
        return body

    def _create_thumbnail(self, path, syntax=None):
        thumbnail_dir = os.path.dirname(path)
        if not os.path.exists(thumbnail_dir):
            os.makedirs(thumbnail_dir)
        if not syntax:
            syntax = self.extension
        try:
            lexer = get_lexer_by_name(syntax)
        except:
            lexer = get_lexer_by_name('text')
        formatter = ImageFormatter(
                font_size=12,
                line_numbers=False
        )
        data = highlight(self.body, lexer, formatter)
        try:
            from PIL import Image
        except:
            import Image
        thumbnail = Image.open(StringIO(data))
        thumbnail = thumbnail.crop((0, 0, 288, 288))
        thumbnail.save(path)
        return path
