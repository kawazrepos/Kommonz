# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

import os
from cStringIO import StringIO
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils.translation import ugettext as _
from apps.licenses.models import CodeLicense
from ..utils.syntaxes import SYNTAXES, guess_syntax
from ..models import Material
from ..managers import MaterialManager

class Code(Material):
    """
    Model for Source Code material.
    """
    syntax = models.CharField(_('Syntax'), max_length='32', choices=SYNTAXES)
    body   = models.TextField(_('Body'), editable=False)

    objects = MaterialManager()

    license_type = CodeLicense
    
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
        if not self._thumbnail:
            path = self._get_thumbnail_path(os.path.basename(self.file.path))
            thumbnail_path = "%s.png" % os.path.splitext(path)[0]
            self._create_thumbnail(path=os.path.join(settings.MEDIA_ROOT, thumbnail_path))
            self._thumbnail = thumbnail_path
            signals.post_save.connect(self._thumbnail.field._create_thumbnails, sender=Code)
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
            syntax = self.syntax.lower()
        try:
            lexer = get_lexer_by_name(syntax)
        except:
            lexer = get_lexer_by_name('text')
        style = get_style_by_name('vs')
        formatter = ImageFormatter(
                style=style,
                font_size=12,
                line_numbers=False
        )
        data = highlight(self.body, lexer, formatter)
        try:
            from PIL import Image
        except ImportError:
            import Image
        thumbnail = Image.open(StringIO(data))
        background = Image.new('RGB', (288, 288), style.background_color)
        thumbnail = thumbnail.crop((0, 0, min(288, thumbnail.size[0]), min(288, thumbnail.size[1])))
        background.paste(thumbnail, (0, 0))
        background.save(path)
        return path
