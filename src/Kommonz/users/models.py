from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext as _
from Kommonz.imagefield.fields import ImageField
import os

class KommonzUser(User):
    '''extended User model for Kommonz'''
    
    def _get_icon_path(self, filename):
        path = u'storage/profiles/%s' % self.username
        return os.path.join(path, filename)
    
    SEX_TYPES = (
        ('man',   _("Man")),
        ('woman', _('Woman'))
    )
    
    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (96, 96, False),
        'middle':   (48, 48, False),
        'small':    (24, 24, False),
    }
    
    # required
    nickname = models.CharField(_('Nickname'), max_length=32, blank=False, null=True)
    remarks  = models.TextField(_('Profile'), blank=False, null=True)                 # it will replace with another markup field.
    
    # not required
    icon            = ImageField(_('Profile Icon'), upload_to=_get_icon_path)
    sex             = models.CharField(_('Sex'), max_length=10, choices=SEX_TYPES, blank=True)
    birthday        = models.DateField(_('Birthday'), null=True, blank=True)
    place           = models.CharField(_('Location'), max_length=255, blank=True)
    url             = models.URLField(_('URL'), max_length=255, blank=True)
    
    objects         = UserManager()
    
    def __unicode__(self):
        return '%s(%s)' % (self.nickname, self.username)
    
    class Meta:
        ordering            = ('username',)
        verbose_name        = _('Kommonz User')
        verbose_name_plural = _('Kommonz Users')