# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from materials.models.base import Material
from materials.models.base import Material
from qwert.middleware.threadlocals import request as get_request


PUB_STATES = (
    ('public',      _('outer publicity')),
    ('protected',   _('inner publicity')),
)


class List(models.Model):
    title             = models.CharField(_('title'), max_length=64)
    author            = models.ForeignKey(User, verbose_name=_('author'),related_name="lists")
    matelials         = models.ManyToManyField(Material, through='ListInfo')
    pub_state         = models.CharField(u"公開設定",max_length=10,choices=PUB_STATES, default="public",)
    created_at        = models.DateTimeField(_('create at'), auto_now_add=True)
    
    class Meta:
        app_label           = 'lists'
        ordering            = ('-created_at',)
        verbose_name        = _('list')
        verbose_name_plural = _('lists')
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('lists_list_detail', (), { 'pk' : self.pk })

    
class ListInfo(models.Model):
    list = models.ForeignKey(List)
    material = models.ForeignKey(Material)
    add_at = models.DateTimeField(_('Add Date'), auto_now_add=True)
    comment = models.CharField(_('Comment'), max_length=128)







