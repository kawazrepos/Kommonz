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
        self.category4 = Category.objects.create(label="Item", parent=self.category1)
        self.category5 = Category.objects.create(label="Bullet", parent=self.category1)
        self.category6 = Category.objects.create(label="Map", parent=self.category2)
        self.category7 = Category.objects.create(label="Town", parent=self.category6)
        self.category8 = Category.objects.create(label="Dungeon", parent=self.category6)
        self.category9 = Category.objects.create(label="Forest", parent=self.category8)
        
    def teardown(self):
        for i in xrange(0, 9):
            category = getattr(self, "category%d" % i)
            category.delete()

    def test_get_children(self):
        """
        Tests manager can get a category's descendants.
        """
        shooting = Category.objects.get_children(self.category1)
        ok_(isinstance(shooting, QuerySet))
        eq_(shooting.count(), 3)
        rpg = Category.objects.get_children(self.category2)
        eq_(rpg.count(), 4)
        forest = Category.objects.get_children(self.category9)
        eq_(forest.count(), 0)

    def test_get_parents(self):
        """
        Tests manager can get a category's parents.
        """
        forest_parents = Category.objects.get_parents(self.category9)
        ok_(isinstance(forest_parents, QuerySet))
        eq_(forest_parents.count(), 4)
        map_parents = Category.objects.get_parents(self.category6)
        eq_(map_parents.count(), 2)
        image_parents = Category.objects.get_parents(self.category0)
        eq_(image_parents.count(), 0)
        
    def test_get_tree(self):
        """
        Tests manager can get a category's dict tree.
        """
        map_category = Category.objects.get(pk=self.category6.pk)
        map_dict = map_category.get_children_tree()
        eq_(map_dict.get('Town'), {})
        eq_(map_dict.get('Dungeon'), {'Forest' : {}})
        
    def test_get_children_json(self):
        """
        Tests manager can get a category's children json.
        """
        map_category = Category.objects.get(pk=self.category6.pk)
        map_json = map_category.get_children_json()
        print map_json
        #not yet
     
        
    def test_get_filetype_category(self):
        """
        Tests manager can get a filename suitable category.
        """
        print Category.objects.all()
        image_category = Category.objects.get_filetype_category("kawaztan.png")
        ok_(isinstance(image_category, Category))
        eq_(image_category.label, 'Image')
        audio_category = Category.objects.get_filetype_category("kawaztan_theme.mp3")
        eq_(audio_category.label, 'Audio')
        code_category = Category.objects.get_filetype_category("create_kawaz.py")
        eq_(code_category.label, 'Code')
        
