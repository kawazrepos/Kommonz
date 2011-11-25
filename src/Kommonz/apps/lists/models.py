# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from apps.materials.models import Material
from qwert.middleware.threadlocals import request as get_request

PUB_STATES = (
    ('public',      _('outer publicity')),
    ('protected',   _('inner publicity')),
)

ORDER_STATES =(
    ('listinfo__add_date',       _('add date')),
    ('downloads_times',          _('downloads times')),
    ('material_upload_date',     _('material upload date')),
    ('author',                   _('auther')),
    ('-listinfo__add_date',      _('listinfo__add_date')),
    ('-download_times',          _('-downloadb times')),
    ('-material_upload_date',    _('-material upload date')),
    ('-author',                  _('-author')),
)


class List(models.Model):
    label             = models.CharField(_('title'), max_length=64)
    author            = models.ForeignKey(User, verbose_name=_('author'),related_name="lists")
    materials         = models.ManyToManyField(Material, through='ListInfo')
    pub_state         = models.CharField(_('public configration'),max_length=10,choices=PUB_STATES, default="public",)
    created_at        = models.DateTimeField(_('create at'), auto_now_add=True)
    order             = models.CharField(_('order'),choices=ORDER_STATES,default="created_date", max_length=64)
    description       = models.CharField(_('introduce comment'), max_length=100)
    
    class Meta:
        ordering            = ['-created_at']
        verbose_name        = _('list')
        verbose_name_plural = _('lists')
    
    def __unicode__(self):
        return self.label
    
    @models.permalink
    def get_absolute_url(self):
        return ('lists_list_detail', (), { 'pk' : self.pk })
    
class ListInfo(models.Model):
    list         = models.ForeignKey(List)
    material     = models.ForeignKey(Material, related_name='listinfo')
    created_at   = models.DateTimeField(_('Add Date'), auto_now_add=True)
    comment      = models.CharField(_('Comment'), max_length=128)
    
    class Meta:
        ordering            = ['-created_at']
        verbose_name        = _('list_info')
        verbose_name_plural = _('list_infos')
    
    def __unicode__(self):
        return self.material.label
        





