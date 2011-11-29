# -*- coding: utf-8 -*-
from nose.tools import *
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test.client import Client
from models import List

class TestListCreate(object):
    def setup(self):
        try:
            self.user = User.objects.create_user(username='kawaztan', password='password', email="test@test.com")
        except:
            self.user = User.objects.get(username='kawaztan')
        try:
            self.user2 = User.objects.create_user(username='kawaztan2', password='password', email="test@test.com")
        except:
            self.user2 = User.objects.get(username='kawaztan2')


    def test_create_list(self):
        """
        Tests user can create list from view.
        """
        c = Client()
        c.login(username='kawaztan', password='password')
        response = c.post(reverse('lists_list_create'), {
            'label': u'STG素材一覧',
            'pub_state' : 'public',
            'order' :'download'
        })
        ok_(List.objects.get(label=u'STG素材一覧'))

    def test_create_permission(self):
        """
        Tests anonymous user can't create list from view.
        """
        count = List.objects.count()
        c = Client()
        response = c.post(reverse('lists_list_create'), {
            'label': u'かわずたん素材集',
            'pub_state' : 'public',
            'order' :'download'
        })
        eq_(count, List.objects.count())

    @raises(IntegrityError)
    def test_duplicate_list(self):
        """
        Tests user can't create duplicate named lists.
        """
        count = List.objects.count()
        c = Client()
        c.login(username='kawaztan', password='password')
        response = c.post(reverse('lists_list_create'), {
            'label': u'RPG素材一覧',
            'pub_state' : 'public',
            'order' :'download'
        })
        eq_(count + 1, List.objects.count())
        c = Client()
        c.login(username='kawaztan2', password='password')
        response = c.post(reverse('lists_list_create'), {
            'label': u'RPG素材一覧',
            'pub_state' : 'public',
            'order' :'download'
        })
        eq_(count + 2, List.objects.count(), 'other user can create exist name list.')
        c = Client()
        c.login(username='kawaztan', password='password')
        response = c.post(reverse('lists_list_create'), {
            'label': u'RPG素材一覧',
            'pub_state' : 'public',
            'order' :'download'
        })
        eq_(count + 2, List.objects.count(), "user can't create duplicate named lists.")


class TestListManage(object):
    def test_add_material(self):
        """
        Tests user can add material from view.
        """

    def test_remove_material(self):
        """
        Tests user can remove material from view.
        """
    
    def test_update_list(self):
        """
        Tests user can update list from view.
        """

    def test_delete_list(self):
        """
        Tests user can delete list from view.
        """

    def test_list_manage_permission(self):
        """
        Tests list owner only can manage lists.
        """

class TestListPublicity(object):
    def test_list_public(self):
        """
        Tests anonymous user can see public list
        """

    def test_list_private(self):
        """
        Tests other user can't see private list
        """

class TestListList(object):
    def test_list_view(self):
        """
        Tests authenticated user can get own lists list.
        """

    def test_anonymous_list(self):
        """
        Tests anonymous user can't get lists list.
        """

class TestListOrder(object):
    def test_order_by_added_ascending(self):
        """
        Tests list shows materials ordered by added date by ascending.
        """

    def test_order_by_added_descending(self):
        """
        Tests list shows materials ordered by added date by descending.
        """

    def test_order_by_download_ascending(self):
        """
        Tests list shows download times ordered by added date by ascending.
        """
    
    def test_order_by_download_descending(self):
        """
        Tests list shows download times ordered by added date by descending.
        """

    def test_order_by_created_ascending(self):
        """
        Tests list shows materials ordered by created date by ascending.
        """

    def test_order_by_created_descending(self):
        """
        Tests list shows materials ordered by created date by descending.
        """

    def test_order_by_author(self):
        """
        Tests list shows materials ordered by author.
        """

class TestZipView(object):
    def test_zip_view(self):
        """
        Tests user can download zipped files of materials in list.
        """
