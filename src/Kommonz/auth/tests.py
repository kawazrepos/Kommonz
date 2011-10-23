from django.test.client import Client
from django.core.urlresolvers import reverse
from nose.tools import *
from models import KommonzUser
from qwert.middleware.threadlocals import request

class TestAuthentication(object):
    
    def test_user_create(self):
        """
            Tests can create KommonzUser
        """
        ok_(KommonzUser.objects.create_user(username='kawaz_inonaka', email='test@test.com'))
    
    def test_login_kommonz_user(self):
        """
            Tests can login with KommonzUser.
        """
        KommonzUser.objects.create_user(username='kawaztan', email='kawaz@kawaz.org', password='pass')
        c = Client()
        ok_(c.login(username='kawaztan', password='pass'))
        
    def test_user_downcast(self):
        """
            Tests create auth.KommonzUser when auth.User created.
        """
        from django.contrib.auth.models import User
        User.objects.create_user(username='kagamin', email='kagamin@gmail.com')
        ok_(KommonzUser.objects.get(username='kagamin'))
        
class TestKommonzUserEquals(object):
    
    def setup(self):
        from django.contrib.auth.models import User
        try:
            self.user = User.objects.create_user(username='miku', email='mikkumiku@gmail.com')
            self.kommonz_user = KommonzUser.objects.get(username='miku')
            self.user2 = User.objects.create_user(username='rin', email='tokachi@gmail.com')
            self.kommonz_user2 = KommonzUser.objects.get(username='rin')
        except:
            self.user = User.objects.get(username='miku')
            self.kommonz_user = KommonzUser.objects.get(username='miku')
            self.user2 = User.objects.get(username='rin')
            self.kommonz_user2 = KommonzUser.objects.get(username='rin')

    def test_user_equals(self):
        """
            Tests __eq__ works well.
        """
        ok_(self.user == self.kommonz_user)
        
    def test_user_equals_different(self):
        """
            Tests __eq__ works well between different Objects.
        """
        ok_(not (self.user == self.user2))
        
class TestKommonzUserMapper(object):
    def test_user_mapper(self):
        from mappers import KommonzUserMapper
        user = KommonzUser.objects.create_user(username='kawaz', email='kawaz@gmail.com')
        user.nickname = 'Kawaz Inonaka'
        user.save()
        mapper = KommonzUserMapper(user)
        dict = mapper.as_dict()
        eq_(dict['nickname'], 'Kawaz Inonaka')