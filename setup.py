#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
short module explanation

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"
__VERSION__ = "0.1.0"
from setuptools import setup, find_packages

def read(filename):
    import os.path
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename).read()

setup(
    name="Kommonz",
    version=__VERSION__,
    description = "Creative Commons Material Collection for Game",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django creative commons",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/kommonz/kommonz.git",
    download_url = r"https://github.com/kommonz/kommonz/tarball/master",
    packages = find_packages(exclude=['ez_setup']),
    include_package_data = True,
    zip_safe = False,
    test_suite='nose.collector',
    tests_require=['Nose'],
    install_requires=[
        'setuptools',
        'setuptools-git',
        'dateutils',
        'docutils',
        'pyyaml',
        'django',
        'django-compress',
        'django-reversetag',
        'django-pagination',
        'django-mfw',
        'django-qwert',
        'django-object-permission',
    ],
)

