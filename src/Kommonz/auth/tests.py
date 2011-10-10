"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

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