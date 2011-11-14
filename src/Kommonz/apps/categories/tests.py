# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/categories/tests.py
# created by giginet on 2011/11/14
#
from django.db.models.query import QuerySet
from django.test.client import Client
from nose.tools import *
from apps.categories.models import Category

class TestCategoryManager(object):
    def setup(self):
        self.category0 = Category.objects.create(label="Image")
        self.category1 = Category.objects.create(label="Shooting", parent=self.category0)
        self.category2 = Category.objects.create(label="RPG", parent=self.category0)
        self.category3 = Category.objects.create(label="Enemy", parent=self.category1)
        self.category5 = Category.objects.create(label="Bullet", parent=self.category1)
        self.category6 = Category.objects.create(label="Map", parent=self.category2)
        self.category7 = Category.objects.create(label="Town", parent=self.category6)
        self.category8 = Category.objects.create(label="Dungeon", parent=self.category6)
        self.category9 = Category.objects.create(label="Forest", parent=self.category8)

    def test_get_children(self):
        """
        Tests manager can get a category's descendants.
        """
        shooting = Category.objects.get_children(self.category1)
        ok_(isinstance(shooting, QuerySet))
        eq_(shooting.count(), 2)
        rpg = Category.objects.get_children(self.category2)
        eq_(rpg.count(), 4)
        forest = Category.objects.get_children(self.category9)
        eq_(forest.count(), 0)
