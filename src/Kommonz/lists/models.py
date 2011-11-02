 # Create your models here.
from materials.models.base import Material
from django.db import models
from django.utils.translation import ugettext as _

PUB_STATES = (
    ('public',      _('outer publicity')),
    ('protected',   _('inner publicity')),
)


class List(models.Model):
    title = models.CharField
    author = models.ForeignKey(KommonzUser, verbose_name=_('author'), editable=False, related_name="materials")
    matelials = models.ManyToManyField(Materials,through='MyListInfo')
    pub_state = models.CharField(u"公開設定",max_length=10,choices=PUB_STATES, default="public",)

class ListInfo(models.Model):
    list = ForeignKey(List)
    material = ForeignKey(Material)
    date = models.DateTimeField
    comment = models.CharField







