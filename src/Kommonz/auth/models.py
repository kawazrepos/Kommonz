from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save, pre_delete
from django.utils.translation import ugettext as _
from imagefield.fields import ImageField
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
        
    def __eq__(self, obj):
        return issubclass(obj.__class__, User) and getattr(self, 'username') == getattr(obj, 'username')
        
def create_kommonz_user(sender, instance, created, **kwargs):
    if created and isinstance(instance, User) and not isinstance(instance, KommonzUser):
        try:
            user = KommonzUser.objects.get(username=instance.username)
        except:
            extended_user = KommonzUser(user_ptr_id=instance.pk)
            extended_user.__dict__.update(instance.__dict__)
            extended_user.save()
            
def delete_kommonz_user(sender, instance, **kwargs):
    if isinstance(instance, User) and not isinstance(instance, KommonzUser):
        try:
            user = KommonzUser.objects.get(username=instance.username)
            user.delete()
        except:
            pass # fail silently.
        
post_save.connect(create_kommonz_user, sender=User)
pre_delete.connect(delete_kommonz_user, sender=User)