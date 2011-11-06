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
        from materials.models.code import Code
        cls = Material.objects.get_file_model('file.py')
        eq_(cls, Code)

    def test_suitable_model_image(self):
        """
            Tests get suitable type from image.
        """
        from materials.models.image import Image
        cls = Material.objects.get_file_model('file.jpg')
        eq_(cls, Image)
        
    def test_suitable_model_others(self):
        """
            Tests get suitable type from filename.
        """
        cls = Material.objects.get_file_model('file.aaa')
        eq_(cls, Material)