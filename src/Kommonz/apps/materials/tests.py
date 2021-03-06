# -*- coding: utf-8 -*-
import os
import re
import tempfile
import shutil
from django.test.client import Client
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import simplejson
from nose.tools import *
from apps.categories.models import Category
from models import Material, MaterialFile
from packages.models import Package

def upload_material(file, username='hogehoge', password='password', **kwargs):
    """
    Create material model from view.
    """
    try:
        user = User.objects.create_user(username=username, password=password, email="test@test.com")
    except:
        user = User.objects.get(username=username)
    c = Client()
    c.login(username=username, password=password)
    response = c.post(reverse('materials_material_file_create'), {'file' : file})
    file_pk = simplejson.loads(response.content)[0]['id']

    kwargs.update({'_file' : file_pk, 
        'license': 100,
        'kero': 1})
    if not kwargs.has_key('category'):
        category, created = Category.objects.get_or_create(label='TestCategory')
        kwargs['category'] = category.pk
    response = c.post(reverse('materials_material_create'), kwargs)
    print response.content
    match = re.search(r'(?P<pk>\d+)/$', response['Location'])
    pk = match.groupdict()['pk']
    return Material.objects.get(pk=pk)

class TestMaterialUtils(object):
    def test_suitable_model_code(self):
        """
        Tests get suitable type from javascript source code.
        """
        from apps.materials.codes.models import Code
        cls = Material.objects.get_file_model('file.js')
        eq_(cls, Code)

    def test_suitable_model_code2(self):
        """
        Tests get suitable type from source code.
        """
        from apps.materials.codes.models import Code
        cls = Material.objects.get_file_model('file.py')
        eq_(cls, Code)

    def test_suitable_model_image(self):
        """
        Tests get suitable type from image.
        """
        from apps.materials.images.models import Image
        cls = Material.objects.get_file_model('file.jpg')
        eq_(cls, Image)

    def test_suitable_model_package(self):
        """
        Tests get suitable type from package.
        """
        from apps.materials.packages.models import Package
        cls = Material.objects.get_file_model('file.zip')
        eq_(cls, Package)
        
    def test_suitable_model_others(self):
        """
        Tests get suitable type from other file.
        """
        cls = Material.objects.get_file_model('file.aaa')
        eq_(cls, Material)

class TestMaterialCode(object):
    def setup(self):
        if not os.path.exists(settings.TEST_TEMPORARY_FILE_DIR):
            os.mkdir(settings.TEST_TEMPORARY_FILE_DIR)

    def test_suitable_syntax(self):
        """
        Tests get suitable syntax type from filename
        """
        from utils.syntaxes import guess_syntax
        syntax = guess_syntax(u'おっ.py')
        eq_(syntax, 'Python')
        syntax = guess_syntax('hoge.coffee')
        eq_(syntax, 'CoffeeScript')

    def test_code_body(self):
        """
        Tests when codefile was uploaded, read file and set as body.
        """
        category = Category.objects.create(label=u"ソースコード")
        f = File(tempfile.NamedTemporaryFile(
            mode="r+w+t", suffix=".py", 
            dir=settings.TEST_TEMPORARY_FILE_DIR
        ))
        
        body = """
            import this
            print "this is a sample code file"
            hoge = 1 + 1
        """
        f.write(body)
        material_file = MaterialFile.objects.create(file=f)
        code = Material.objects.create(
                _file=material_file, 
                description="description", 
                category=category
        )
        print code.body
        f.close()
        eq_(code.body, body)
        code.delete()

class TestMaterialUpload(object):
    def setup(self):
        if not os.path.exists(settings.TEST_TEMPORARY_FILE_DIR):
            os.mkdir(settings.TEST_TEMPORARY_FILE_DIR)
        Category.objects.create(label=u"現代医学の敗北シリーズ")

    def teardown(self):
        if os.path.exists(settings.TEST_TEMPORARY_FILE_DIR):
            shutil.rmtree(settings.TEST_TEMPORARY_FILE_DIR)
        os.mkdir(settings.TEST_TEMPORARY_FILE_DIR)

    def test_auto_cast_material_type_code(self):
        """
        Test cast material model to suitable type when code file was uploaded.
        """
        from apps.materials.codes.models import Code
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

    def test_auto_cast_material_type_other(self):
        """
        Tests cast material model to suitable type when other file was uploaded.
        """
        from apps.materials.models import Material
        test_file = File(tempfile.NamedTemporaryFile(
            mode="r+w+t", suffix=".hoge", 
            dir=settings.TEST_TEMPORARY_FILE_DIR
        ))
        test_file.write("hello!hello!")
        material_file = MaterialFile.objects.create(file=test_file)
        material = Material.objects.create(
                _file=material_file, 
                description="description", 
                category=Category.objects.get(pk=1)
        )
        ok_(isinstance(material, Material))
        test_file.close()

class TestMaterialUpload(object):
    def setup(self):
        category = Category.objects.create(label=u"かわずたん")
        self.username = 'hogehoge'
        self.filename = 'kawaztan.png'
        f = open(os.path.join(settings.TEST_FIXTURE_FILE_DIR, self.filename), 'rb')
        self.material = upload_material(f, username=self.username,
                label=u"かわずたん",
                description=u"かわずたんアイコン",
                category=category.pk
        )

    def teardown(self):
        if self.material.pk:
            self.material.delete()

    def test_upload_from_view(self):
        """
        Tests user can upload materials from view.
        """
        ok_(os.path.exists(self.material.file.path))

    def test_material_file_deletion(self):
        """
        Tests material was deleted. It's file will delete together.
        """
        self.material.delete()
        ok_(not os.path.exists(os.path.dirname(self.material.file.path)))

class TestMaterialPackage(object):
    def setup(self):
        if not os.path.exists(settings.TEST_TEMPORARY_FILE_DIR):
            os.mkdir(settings.TEST_TEMPORARY_FILE_DIR)
        category = Category.objects.create(label=u"かわずたん")
        f = open(os.path.join(settings.TEST_FIXTURE_FILE_DIR, 'kawazicon.zip'), 'rb')
        self.package = upload_material(f,
                label=u"かわずたんアイコン詰め合わせ",
                description=u"かわずたん詰め合わせ",
                category=category.pk
        )
        self.package = Package.objects.get(pk=self.package.pk)

    def test_package_extract(self):
        """
        Tests extract zipped file and create new material from them.
        """
        from images.models import Image
        self.package.extract_package()
        filename = os.path.basename(self.package.file.name)
        material_path = os.path.dirname(self.package.file.path)
        ok_(os.path.exists(os.path.join(material_path, 'kawazicon', 'icon0.png')))
        eq_(self.package.materials.count(), 12)

        for image in self.package.materials.iterator():
            ok_(image.model == Image)

    def test_package_extract_recursively(self):
        """
        Tests extract zipped file and create new packages recursively.
        """
        self.package.extract_package(recursive=True)
        filename = os.path.basename(self.package.file.name)
        material_path = os.path.dirname(self.package.file.path)
        ok_(os.path.exists(os.path.join(material_path, 'kawazicon', 'icon0.png')))
        eq_(self.package.materials.count(), 14)

    def teardown(self):
        self.package.delete()
