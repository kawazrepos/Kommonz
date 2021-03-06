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
        User.objects.create_user(username='kawaztan', email='kawaz@kawaz.org', password='password')
        c = Client()
        ok_(c.login(username='kawaztan', password='password'))
        
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
            self.kawaz = User.objects.create_user(username='kawaztan2', email='kawaztan@kawaz.org', password='password')
        except:
            self.kawaz = User.objects.get(username='kawaztan2')

    def test_thumbnail(self):
        """
        Tests thumbnails are resized automatically when user profile was updated.
        """
        import os
        c = Client()
        ok_(c.login(username='kawaztan2', password='password'))
        avatar = open(os.path.join(settings.TEST_FIXTURE_FILE_DIR, 'kawaztan.png'), 'rb')
        c.post(reverse('auth_userprofile_update'), {
            'nickname' : u'かわずたん',
            'description' : u'来てっ！',
            '_avatar' : avatar
        })
        eq_(self.kawaz.profile.nickname, u'かわずたん')
        ok_(self.kawaz.profile._avatar.small)
        small_avatar = self.kawaz.profile._avatar.small.path
        ok_(os.path.exists(small_avatar))

    def test_thumbnail_deletion(self):
        """
        Tests UserProfile.clean_up__avatar works well.
        """
        import os
        from models import USER_ICON_PATH
        avatar_dir = os.path.join(settings.ROOT, USER_ICON_PATH, self.kawaz.username)
        self.kawaz.profile.clean_up_avatar()
        ok_(not os.path.exists(avatar_dir))

    def teardown(self):
        self.kawaz.profile.clean_up_avatar()
