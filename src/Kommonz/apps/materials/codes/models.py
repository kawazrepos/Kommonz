# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
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
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Code')
        verbose_name_plural = _('Codes')
    
    def clean(self):
        if not self.syntax:
            self.syntax = self._guess_syntax()
        super(Code, self).clean()

    def save(self, *args, **kwargs):
        post_save.connect(set_body, sender=Code)
        super(Code, self).save(*args, **kwargs)

    def _guess_syntax(self):
        """
        Guess a programming language from the filename
        """
        return guess_syntax(self.file.name)

def set_body(sender, instance, created, **kwargs):
    code = open(instance.file.path)
    instance.body = code.read()
    code.close()
