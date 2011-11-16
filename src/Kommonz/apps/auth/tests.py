# -*- coding: utf-8 -*-
from nose.tools import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test.client import Client
from models import UserProfile, UserOption

class TestAuthentication(object):
    
    def test_user_creation(self):
        """
        Tests can create User
        """
        ok_(User.objects.create_user(username='kawaz_inonaka', email='test@test.com'))
    
    def test_login_user(self):
        """
        Tests can login with User.
        """
        User.objects.create_user(username='kawaztan', email='kawaz@kawaz.org', password='pass')
        c = Client()
        ok_(c.login(username='kawaztan', password='pass'))
        
    def test_auto_profile_creation(self):
        """
        Tests create UserProfile and UserOption when auth.User created.
        """
        kagamin = User.objects.create_user(username='kagamin', email='kagamin@example.com')
        ok_(UserProfile.objects.get(user=kagamin))
        ok_(UserOption.objects.get(user=kagamin))

        
class TestUserProfileMapper(object):
    def test_user_mapper(self):
        """
        Tests UserProfileMapper dumps user profile to a dictionary well.
        """
        from mappers import UserProfileMapper
        user = User.objects.create_user(username='kawaz', email='kawaz@kawaztan.com')
        user.profile.nickname = 'Kawaz Inonaka'
        user.save()
        mapper = UserProfileMapper(user.profile)
        test_dict = mapper.as_dict()
        eq_(test_dict['nickname'], 'Kawaz Inonaka')

class TestUserThumbnail(object):
    def setup(self):
        try:
            from PIL import Image, ImageOps
        except ImportError:
            import Image
            import ImageOps
        import tempfile
        icon = Image.new('RGBA', (512, 512))
        self.icon_file = tempfile.NamedTemporaryFile(
                mode="r+w+b",
                suffix=".png",
                dir=settings.TEST_TEMPORARY_FILE_DIR
        )
        icon.save(self.icon_file)

    def test_thumbnail_resizing(self):
        """
        Tests thumbnails are resized automatically when user profile was updated.
        """
        kawaz = User.objects.create_user(username='kawaztan2', email='kawaztan@kawaz.org', password='password')
        c = Client()
        c.login(username='kawaztan2', password='pass')
        response = c.post(reverse('auth_userprofile_update'), {
            'nickname' : u'かわずたん',
            'description' : u'来てっ！',
            'icon' : self.icon_file
        })

