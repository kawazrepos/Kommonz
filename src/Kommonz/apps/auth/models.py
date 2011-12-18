import os
import shutil
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.db.models.fields.files import ImageFieldFile
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext as _
from fields.thumbnailfield.fields import ThumbnailField

USER_ICON_PATH = os.path.join('storage', 'profiles')
DEFAULT_ICON_PATH = os.path.join('image', 'default', 'avatar', 'avatar.png')

class UserProfile(models.Model):
    """
    A model for User profile.
    """
    def _get_avatar_path(self, filename):
        path = os.path.join(USER_ICON_PATH, self.user.username)
        return os.path.join(path, filename)
    
    SEX_TYPES = (
        ('man',   _("Man")),
        ('woman', _('Woman'))
    )
    
    AVATAR_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (144, 144, False),
        'middle':   (96, 96, False),
        'small':    (27, 27, False),
    }
    
    # required
    user        = models.OneToOneField(User, related_name='profile')
    nickname    = models.CharField(_('Nickname'), max_length=32, blank=False, null=True)
    description = models.TextField(_('Profile Text'), blank=False, null=True)
    
    # not required
    _avatar      = ThumbnailField(_('Profile Icon'), upload_to=_get_avatar_path, thumbnail_size_patterns=AVATAR_SIZE_PATTERNS)
    sex          = models.CharField(_('Sex'), max_length=10, choices=SEX_TYPES, blank=True)
    birthday     = models.DateField(_('Birthday'), null=True, blank=True)
    place        = models.CharField(_('Location'), max_length=255, blank=True)
    url          = models.URLField(_('URL'), max_length=255, blank=True)    
    
    objects      = UserManager()
    
    def __unicode__(self):
        if self.nickname:
            return '%s(%s)' % (self.nickname, self.user.username)
        return self.user.username
    
    class Meta:
        verbose_name        = _('User Profile')
        verbose_name_plural = _('User Profiles')
        
    @models.permalink
    def get_absolute_url(self):
        return ('auth_user_detail', (), { 'pk' : self.id })
    
    @property
    def avatar(self):
        """
        Returns own avatar or default avatar.
        """
        if self._avatar:
            return self._avatar
        return DefaultAvatarFile(self, self._avatar.field)

    def clean_up_avatar(self):
        avatar_dir = os.path.dirname(self._avatar.path)
        if os.path.exists(avatar_dir):
            shutil.rmtree(avatar_dir)
        
class UserOption(models.Model):
    user = models.OneToOneField(User, related_name='option')
    
    email_notification = models.BooleanField(_('Email Notification'), default=True)
    
    class Meta:
        verbose_name        = _('User Option')
        verbose_name_plural = _('User Options')
        
    @models.permalink
    def get_absolute_url(self):
        return ('auth_useroption_update', (), {})

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def create_user_option(sender, instance, created, **kwargs):
    if created:
        UserOption.objects.get_or_create(user=instance)

class DefaultAvatarFile(ImageFieldFile):
    """
    Default avatar Image class
    """
    def __init__(self, instance, field):
        super(DefaultAvatarFile, self).__init__(instance, field, DEFAULT_ICON_PATH)
        for pattern_name, pattern_size in UserProfile.AVATAR_SIZE_PATTERNS.iteritems():
            path, ext = os.path.splitext(DEFAULT_ICON_PATH)
            setattr(self, pattern_name, ImageFieldFile(instance, field, "%s.%s%s" % (path, pattern_name, ext)))
