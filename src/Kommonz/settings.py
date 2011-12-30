# -*- coding: utf-8 -*-
# Django settings for Kommonz project.

# Load pre local_settings
import os
import sys
from utils import lazy_reverse

try:
    from local_site import *
except ImportError:
    LOCAL_SITE_LOADED = False
ROOT = os.path.join(os.path.dirname(__file__), '../../')
#--- Add PYTHON_PATH ---------------------------------
PYTHON_PATHS = (
    os.path.join(ROOT, 'src/libs'),
)
for path in PYTHON_PATHS:
    if path not in sys.path: sys.path.append(path)
#-----------------------------------------------------

    
# Version of Kommonz
VERSION = '0.0'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',   # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':     os.path.join(ROOT, 'kommonz.db'), # Or path to database file if using sqlite3.
        'USER':     '',                             # Not used with sqlite3.
        'PASSWORD': '',                             # Not used with sqlite3.
        'HOST':     '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT':     '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# django-storages File Storage Settings
DB_FILES_URL = os.path.join(ROOT, 'storage.db')
DB_FILES = {
            'db_table'     : 'files',
            'fname_column' : 'filename',
            'blob_column'  : 'blob',
            'size_column'  : 'size'
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ja'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../../static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT, 'static/collected')

# Make this unique, and don't share it with anybody.
SECRET_KEY = "Make this unique, and don't share it with anybody."

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'qwert.middleware.threadlocals.ThreadLocalsMiddleware',
    'qwert.middleware.http.Http403Middleware',
    'qwert.middleware.exception.UserBasedExceptionMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)

ROOT_URLCONF = 'Kommonz.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT, 'templates'),
    os.path.join(ROOT, 'templates/default'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # Third-party libraries
    'django_nose',                  # UnitTest using nose library
    'social_auth',                  # login with oAuth/OpenID library
    'compress',                     # JavaScript/CSS compress library
    'reversetag',                   # Useful templatetag library
    'pagination',                   # Useful pagination library
    'uni_form',
    'universaltag',                 # Useful tagging library
    # Github libraries
    'qwert',                        # Useful snippet collection library
    'object_permission',            # Object permission library
    # Kommonz
    'Kommonz.autocmd',
    'Kommonz.templatetags',
    'Kommonz.utils',
    # Kommonz apps
    'Kommonz.apps.auth',
    'Kommonz.apps.categories',
    'Kommonz.apps.comments',
    'Kommonz.apps.licenses',
    'Kommonz.apps.lists',
    'Kommonz.apps.materials',
    'Kommonz.apps.messages',
    'Kommonz.apps.keros',
    'Kommonz.apps.notifications',
    'Kommonz.apps.reports',
    'Kommonz.apps.searches',
    # Kommonz materials
    'Kommonz.apps.materials.applications',
    'Kommonz.apps.materials.audios',
    'Kommonz.apps.materials.cgmodels',
    'Kommonz.apps.materials.codes',
    'Kommonz.apps.materials.images',
    'Kommonz.apps.materials.movies',
    'Kommonz.apps.materials.packages',
    'Kommonz.apps.materials.texts'
)

AUTHENTICATION_BACKENDS = (
    'qwert.backends.auth.EmailAuthBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    'social_auth.backends.contrib.orkut.OrkutBackend',
    'social_auth.backends.contrib.foursquare.FoursquareBackend',
    'social_auth.backends.contrib.github.GithubBackend',
#    'social_auth.backends.contrib.dropbox.DropboxBackend', # not available on django-social-auth stable version yet.
    'social_auth.backends.OpenIDBackend',
    'apps.registration.backends.hatena.HatenaBackend',
    'django.contrib.auth.backends.ModelBackend',
    'object_permission.backends.ObjectPermBackend',
)

AUTH_PROFILE_MODULE = 'auth.UserProfile'

#
# SocialAuth Setting
#
SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter', 'google-oauth2', 'github', 'dropbox', 'hatena',)

LOGIN_ERROR_URL     = lazy_reverse('registration_error')
LOGIN_REDIRECT_URL  = "/"
LOGIN_URL           = lazy_reverse('registration_index')
LOGOUT_URL          = lazy_reverse('registration_logout')

SOCIAL_AUTH_NEW_USER_REDIRECT_URL        = lazy_reverse('registration_welcome')
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = lazy_reverse('auth_useraccount_update')
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL      = lazy_reverse('auth_useraccount_update')
SOCIAL_AUTH_ERROR_KEY                    = 'social_errors'

SOCIAL_AUTH_IMPORT_BACKENDS = ('apps.registration.backends', )

#
# ObjectPermission setting
#
OBJECT_PERMISSION_DEPRECATED = True

#
# ThumbnailField setting
#
THUMBNAILFIELD_THUMBNAIL_FILENAME = 'thumbnail'

#
# Testing configuration via nose.
#
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['-v', '-d']
TEST_TEMPORARY_FILE_DIR = os.path.join(ROOT, "static/test/temporary")
TEST_FIXTURE_FILE_DIR = os.path.join(ROOT, "static/fixtures")

#
# django.contrib.comments
#----------------------------------------------------------------------------
COMMENTS_APP = 'Kommonz.apps.comments'
COMMENTS_HIDE_REMOVED = False

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Load local_settings
try:
    from local_settings import *
except ImportError:
    LOCAL_SETTINGS_LOADED = False
