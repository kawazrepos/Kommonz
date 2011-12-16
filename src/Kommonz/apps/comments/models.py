from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _
from apps.materials.models import Material
from qwert.middleware.threadlocals import request as get_request


class MaterialComment(models.Model):
    u"""
        Comment for materials.
    """
    
    author      = models.ForeignKey(User, verbose_name=_('Author'), editable=False, related_name='comments')
    material    = models.ForeignKey(Material, verbose_name=_('Material'), related_name='comments')
    body        = models.TextField(_('Body'))
    
    # auto add
    created_at  = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at  = models.DateTimeField(_('Updated At'), auto_now=True)
    
    def __unicode__(self):
        return 'comment by %s' % self.author
    
    
    def clean(self):
        request = get_request()
        if request.user.is_authenticated():
            self.author = request.user
        else:
            raise ValidationError(_('''Can not create a comment without authenticate'''))
        return super(MaterialComment, self).clean()