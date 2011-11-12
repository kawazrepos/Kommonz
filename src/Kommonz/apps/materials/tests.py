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
from apps.categories.models import Category
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

class TestMaterialUpload(object):
    def setup(self):
        if not os.path.exists(settings.TEST_TEMPORARY_FILE_DIR):
            os.mkdir(settings.TEST_TEMPORARY_FILE_DIR)
        Category.objects.create(label=u"現代医学の敗北シリーズ")

    def test_auto_cast_material_type(self):
        """
        Test cast material model to suitable type when file was uploaded.
        """
        from apps.materials.models.code import Code
        test_file = File(tempfile.NamedTemporaryFile(
            mode="r+w+t", suffix=".py", 
            dir=settings.TEST_TEMPORARY_FILE_DIR
        ))
        test_file.write("hello!hello!")
        material_file = MaterialFile.objects.create(file=test_file)
        material = Material.objects.create(
                _file=material_file, 
                description="description", 
                category=Category.objects.get(pk=1)
        )
        ok_(isinstance(material, Code))
        test_file.close()

    def teardown(self):
        if os.path.exists(settings.TEST_TEMPORARY_FILE_DIR):
            for file in os.listdir(settings.TEST_TEMPORARY_FILE_DIR):
                os.remove(os.path.join(settings.TEST_TEMPORARY_FILE_DIR, file))
