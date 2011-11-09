from django.core.urlresolvers import reverse
from django.test.client import Client
from nose.tools import *
from auth.models import UserProfile, UserOption
from models import User


class TestAuthentication(object):
    
    def test_user_create(self):
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
        
    def test_user_downcast(self):
        """
            Tests create UserProfile and UserOption when auth.User created.
        """
        kagamin = User.objects.create_user(username='kagamin', email='kagamin@gmail.com')
        ok_(UserProfile.objects.get(user=kagamin))
        ok_(UserOption.objects.get(user=kagamin))

        
class TestUserProfileMapper(object):
    def test_user_mapper(self):
        from mappers import UserProfileMapper
        user = User.objects.create_user(username='kawaz', email='kawaz@gmail.com')
        user.profile.nickname = 'Kawaz Inonaka'
        user.save()
        mapper = UserProfileMapper(user.profile)
        dict = mapper.as_dict()
        eq_(dict['nickname'], 'Kawaz Inonaka')