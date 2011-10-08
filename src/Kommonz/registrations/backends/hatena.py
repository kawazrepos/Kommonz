# -*- coding: utf-8 -*-
"""
Hatena OpenID support
ref : http://developer.hatena.ne.jp/ja/documents/auth/apis/oauth/consumer
"""
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/08'
import logging
logger = logging.getLogger(__name__)

from django.utils import simplejson
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME

# Hatena configuration
HATENA_SERVER = 'hatena.com'
HATENA_REQUEST_TOKEN_URL = 'https://%s/oauth/initiate' % HATENA_SERVER
HATENA_ACCESS_TOKEN_URL = 'https://%s/oauth/token' % HATENA_SERVER
HATENA_AUTHORIZATION_URL = 'https:///www.hatena.ne.jp/oauth/authorize'
HATENA_CHECK_AUTH = 'http://n.hatena.com/applications/my.json'


class HatenaBackend(OAuthBackend):
    """Hatena OAuth authentication backend"""
    name = 'hatena'
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Hatena account"""
        return {USERNAME: response['url_name'],
                'email': '',  # not supplied
                'fullname': response['display_name'],
                'first_name': '',
                'last_name': ''
        }


class HatenaAuth(ConsumerBasedOAuth):
    """Hatena OAuth authentication mechanism"""
    AUTHORIZATION_URL = HATENA_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = HATENA_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = HATENA_ACCESS_TOKEN_URL
    SERVER_URL = HATENA_SERVER
    AUTH_BACKEND = HatenaBackend
    SETTINGS_KEY_NAME = 'HATENA_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'HATENA_CONSUMER_SECRET'

    def user_data(self, access_token):
        """Return user data provided"""
        request = self.oauth_request(access_token, HATENA_CHECK_AUTH)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except ValueError:
            return None


# Backend definition
BACKENDS = {
    'hatena': HatenaAuth,
}