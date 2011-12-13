# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from qwert.middleware.threadlocals import request as get_request
from apps.materials.models import Material

PUB_STATES = (
    ('public',      _('Public')),
    ('private',     _('Private')),
)

ORDER_STATES =(
    ('listinfo__created_at',     _('Add Date(Ascending)')),
    ('download',                 _('Download times(Ascending)')),
    ('created_at',               _('Create Date(Ascending)')),
    ('-listinfo__created_at',    _('Add Date(Descending)')),
    ('-download',                _('Download times(Descending)')),
    ('-created_at',              _('Create Date(Descending)')),
    ('author__pk',               _('Author')),
)

class List(models.Model):
    """
    A Model for Material collection.
    """
    # required
    label             = models.CharField(_('title'), max_length=64)
    pub_state         = models.CharField(_('publicity'), max_length=10, choices=PUB_STATES, default="public",)
    order             = models.CharField(_('order'), choices=ORDER_STATES, default="created_date", max_length=64)
    # not required
    description       = models.TextField(_('description'), null=True, blank=True)
    # not editable
    author            = models.ForeignKey(User, verbose_name=_('author'), related_name="lists", editable=False)
    _materials        = models.ManyToManyField(Material, through='ListInfo', editable=False)
    created_at        = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at        = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        ordering            = ['-created_at']
        unique_together     = ('author', 'label')
        verbose_name        = _('list')
        verbose_name_plural = _('lists')
    
    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        request = get_request()
        if request and request.user.is_authenticated():
            self.author = getattr(request, 'user', User.objects.get(pk=1))
        super(List, self).save(*args, **kwargs)
    
    @property
    def materials(self):
        """
        Returns a QuerySet ordered by 'order' field value.
        """
        return self._materials.order_by(self.order)

    @models.permalink
    def get_absolute_url(self):
        return ('lists_list_detail', (), { 'pk' : self.pk })

    def modify_object_permission(self, mediator, created):
        mediator.manager(self, self.author)
        if self.pub_state == 'public':
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')
        elif self.pub_state == 'private':
            mediator.reject(self, None)
            mediator.reject(self, 'anonymous')
    
class ListInfo(models.Model):
    """
    A Model for relational information between List and Material.
    """
    list         = models.ForeignKey(List)
    material     = models.ForeignKey(Material, related_name='listinfo')
    created_at   = models.DateTimeField(_('Add Date'), auto_now_add=True)
    comment      = models.CharField(_('Comment'), max_length=128, null=True, blank=True)
    
    class Meta:
        ordering            = ['-created_at']
        unique_together     = ('list', 'material')
        verbose_name        = _('list_info')
        verbose_name_plural = _('list_infos')
    
    def __unicode__(self):
        return self.material.label

    @models.permalink
    def get_absolute_url(self):
        return ('lists_list_detail', (), { 'pk' : self.list.pk })
