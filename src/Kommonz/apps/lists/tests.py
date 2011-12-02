# -*- coding: utf-8 -*-
import os
from nose.tools import *
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test.client import Client
from apps.materials.tests import upload_material
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
    def setup(self):
        try:
            self.user = User.objects.create_user(username='kawaztan', password='password', email="test@test.com")
        except:
            self.user = User.objects.get(username='kawaztan')
        try:
            self.user2 = User.objects.create_user(username='kawaztan2', password='password', email="test@test.com")
        except:
            self.user2 = User.objects.get(username='kawaztan2')
        self.c = Client()
        self.c.login(username='kawaztan', password='password')
        self.ls = List.objects.get_or_create(
                label='ham',
                pub_state='public',
                order='download',
                description='desc',
                author=self.user
        )[0]
        f = open(os.path.join(settings.TEST_FIXTURE_FILE_DIR, 'kawaztan.png'), 'rb')
        self.material = upload_material(f,
                label="kawaztan.png",
                description="Kawaz tan is so cute.",
        )

    def test_add_material(self):
        """
        Tests user can add material from view.
        """
        self.c.post(reverse('lists_list_add', args=[self.ls.pk]), {
            'material' : self.material.pk
        })
        eq_(self.ls.materials.count(), 1)

    def test_remove_material(self):
        """
        Tests user can remove material from view.
        """
        self.c.post(reverse('lists_list_add', args=[self.ls.pk]), {
            'material' : self.material.pk
        })

        self.c.post(reverse('lists_list_remove', args=[self.ls.pk]), {
            'materials' : [self.material.pk,]
        })
        eq_(self.ls.materials.count(), 0)

    
    def test_update_list(self):
        """
        Tests user can update list from view.
        """
        response = self.c.post(reverse('lists_list_update', args=[self.ls.pk]), {
            'label' : 'spam',
            'pub_state' : self.ls.pub_state,
            'order' : self.ls.order
        })
        self.ls = List.objects.get(pk=self.ls.pk)
        eq_(self.ls.label, 'spam')

    def test_delete_list(self):
        """
        Tests user can delete list from view.
        """
        count = List.objects.count()
        self.c.post(reverse('lists_list_delete', args=[self.ls.pk]))
        eq_(List.objects.count(), count - 1)

    def test_list_manage_permission(self):
        """
        Tests list owner only can manage lists.
        """
        self.c.logout()
        response = self.c.post(reverse('lists_list_update', args=[self.ls.pk]), {
            'label' : 'spamspam',
            'pub_state' : self.ls.pub_state,
            'order' : self.ls.order
        })
        self.ls = List.objects.get(pk=self.ls.pk)
        eq_(self.ls.label, 'ham')

class TestListPublicity(object):
    def setup(self):
        try:
            self.user = User.objects.create_user(username='kawaztan', password='password', email="test@test.com")
        except:
            self.user = User.objects.get(username='kawaztan')
        try:
            self.user2 = User.objects.create_user(username='kawaztan2', password='password', email="test@test.com")
        except:
            self.user2 = User.objects.get(username='kawaztan2')
        self.c = Client()
        self.c.login(username='kawaztan', password='password')
        self.ls = List.objects.get_or_create(
                label='ham',
                pub_state='public',
                order='download',
                description='desc',
                author=self.user
        )[0]

    def test_list_public(self):
        """
        Tests anonymous user can see public list
        """
        self.c.logout()
        response = self.c.get(reverse('lists_list_detail', args=[self.ls.pk]))
        eq_(response.status_code, 200)
        
    def test_list_private(self):
        """
        Tests other user can't see private list
        """
        ls2 = List.objects.get_or_create(
                label='hamhamspam',
                pub_state='private',
                order='download',
                description='desc',
                author=self.user
        )[0]
        self.c.login(username='kawaztan2', password='password')
        response = self.c.get(reverse('lists_list_detail', args=[ls2.pk]))
        eq_(response.status_code, 403)
        
class TestListList(object):
    def setup(self):
        try:
            self.user = User.objects.create_user(username='kawaztan', password='password', email="test@test.com")
        except:
            self.user = User.objects.get(username='kawaztan')
        try:
            self.user2 = User.objects.create_user(username='kawaztan2', password='password', email="test@test.com")
        except:
            self.user2 = User.objects.get(username='kawaztan2')
        self.c = Client()
        self.c.login(username='kawaztan', password='password')
        self.ls = List.objects.get_or_create(
                label='ham',
                pub_state='public',
                order='download',
                description='desc',
                author=self.user
        )[0]

    def test_list_view(self):
        """
        Tests authenticated user can get own lists list.
        """
        self.c.login(username='kawaztan2', password='password')
        ls2 = List.objects.create(
            label='hamham',
            pub_state='public',
            order='download',
            author=self.user2
        )
        count = List.objects.filter(author=self.user2).count()
        response = self.c.get(reverse('lists_list_list'))
        list_list = response.context['object_list']
        eq_(list_list.count(), count)

    def test_anonymous_list(self):
        """
        Tests anonymous user can't get lists list.
        """
        self.c.logout()
        response = self.c.get(reverse('lists_list_list'))
        ok_(not hasattr(response.context, 'object_list'))

@nottest
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

@nottest
class TestZipView(object):
    def test_zip_view(self):
        """
        Tests user can download zipped files of materials in list.
        """
