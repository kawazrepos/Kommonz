import os
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from imagefield.fields import ImageField


class UserProfile(models.Model):
    def _get_icon_path(self, filename):
        path = u'storage/profiles/%s' % self.user.username
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
    user        = models.OneToOneField(User, related_name='profile')
    nickname    = models.CharField(_('Nickname'), max_length=32, blank=False, null=True)
    description = models.TextField(_('Profile Text'), blank=False, null=True)
    
    # not required
    icon         = ImageField(_('Profile Icon'), upload_to=_get_icon_path)
    sex          = models.CharField(_('Sex'), max_length=10, choices=SEX_TYPES, blank=True)
    birthday     = models.DateField(_('Birthday'), null=True, blank=True)
    place        = models.CharField(_('Location'), max_length=255, blank=True)
    url          = models.URLField(_('URL'), max_length=255, blank=True)
    
    # auto set and uneditable
    slug         = models.SlugField(_('Slug'), max_length=30, editable=False)
    
    objects      = UserManager()
    
    def __unicode__(self):
        if self.nickname:
            return '%s(%s)' % (self.nickname, self.user.username)
        return self.user.username
    
    def save(self, force_insert=False, force_update=False, using=None):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(force_insert=force_insert, force_update=force_update, using=using)
    
    class Meta:
        verbose_name        = _('User Profile')
        verbose_name_plural = _('User Profiles')
        
    @models.permalink
    def get_absolute_url(self):
        return ('auth_user_detail', (), { 'slug' : self.slug })
    
        
class UserOption(models.Model):
    user = models.OneToOneField(User, related_name='option')
    
    email_notification = models.BooleanField(_('Email Notification'), default=True)
    
    class Meta:
        verbose_name        = _('User Option')
        verbose_name_plural = _('User Options')
        
    @models.permalink
    def get_absolute_url(self):
        return ('auth_useroption_update', (), {})


# signal callbacks below

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def create_user_option(sender, instance, created, **kwargs):
    if created:
        UserOption.objects.get_or_create(user=instance)