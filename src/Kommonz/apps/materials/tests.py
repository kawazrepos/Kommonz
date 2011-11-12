# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
import tempfile
from django.test.client import Client
from django.core.files.base import File
from django.conf import settings
from nose.tools import *
from models.base import Material, MaterialFile

class TestMaterialUtils(object):
    def test_suitable_model_code(self):
        """
            Tests get suitable type from sourcecode.
        """
        from apps.materials.models.code import Code
        cls = Material.objects.get_file_model('file.py')
        eq_(cls, Code)

    def test_suitable_model_image(self):
        """
            Tests get suitable type from image.
        """
        from apps.materials.models.image import Image
        cls = Material.objects.get_file_model('file.jpg')
        eq_(cls, Image)
        
    def test_suitable_model_others(self):
        """
            Tests get suitable type from filename.
        """
        cls = Material.objects.get_file_model('file.aaa')
        eq_(cls, Material)

class TestCode(object):
    def test_suitable_syntax(self):
        """
            Tests get suitable syntax type from filename
        """
        from utils.syntaxes import guess_syntax
        syntax = guess_syntax(u'おっ.py')
        eq_(syntax, 'Python')
        syntax = guess_syntax('hoge.coffee')
        eq_(syntax, 'CoffeeScript')

class TestMaterialTypeCast(object):
    def setup(self):
        if not os.path.exists(settings.TEST_TEMPORARY_FILE_DIR):
            os.mkdir(settings.TEST_TEMPORARY_FILE_DIR)

    def test_auto_cast_material_type(self):
        from apps.materials.models.code import Code
        test_file = File(tempfile.NamedTemporaryFile(mode="r+w+t", suffix=".py", dir=settings.TEST_TEMPORARY_FILE_DIR))
        test_file.write("hello!hello!")
        test_file.seek(0)
        material_file = MaterialFile.objects.create(file=test_file)
        material = Material.objects.create(label="hoge.py", _file=material_file, description="description", category=Category)
        ok_(isinstance(material, Code))
