# -*- coding: utf-8 -*-
from materials.models.base import Material
from django.db import models
from django.utils.translation import ugettext as _
from auth.models import KommonzUser
from materials.models.base import Material

PUB_STATES = (
    ('public',      _('outer publicity')),
    ('protected',   _('inner publicity')),
)


class List(models.Model):
    title = models.CharField(_('title'), max_length=64)
    author = models.ForeignKey(KommonzUser, verbose_name=_('author'), editable=False, related_name="lists")
    matelials = models.ManyToManyField(Material, through='ListInfo')
    pub_state = models.CharField(u"公開設定",max_length=10,choices=PUB_STATES, default="public",)

class ListInfo(models.Model):
    list = models.ForeignKey(List)
    material = models.ForeignKey(Material)
    add_at = models.DateTimeField(_('Add Date'), auto_now_add=True)
    comment = models.CharField(_('Comment'), max_length=128)







