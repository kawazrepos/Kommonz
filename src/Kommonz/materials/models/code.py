# -*- coding: utf-8 -*-
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/10'

from django.db import models
from django.utils.translation import ugettext as _
from base import Material

class Code(Material):
    """
        Model for Source Code material.
    """
    
    language = models.CharField(_('Syntax'), max_length='32')
    
    class Meta:
        app_label           = 'materials'
        verbose_name        = _('Code')
        verbose_name_plural = _('Codes')
    
    def _guess_language(self):
        """guess a programming language from the filename"""
        # has not implemented