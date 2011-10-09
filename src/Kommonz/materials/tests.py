"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test.client import Client
from nose.tools import *
from models.base import Material

class TestMaterial(object):
    def test_suitable_model_code(self):
        """
            Tests get suitable type from sourcecode.
        """
        from Kommonz.materials.models.code import Code
        cls = Material.objects._get_file_class('file.py')
        eq_(cls, Code)
        
    def test_suitable_model_others(self):
        """
            Tests get suitable type from filename.
        """
        cls = Material.objects._get_file_class('file.aaa')
        eq_(cls, Material)