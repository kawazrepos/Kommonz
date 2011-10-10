# -*- coding: utf-8 -*-
"""
Hatena OpenID support
This is a custom backend for django-social-auth. This adds support for Hatena oauth service.
An application must be registered first on hatena and the settings HATENA_CONSUMER_KEY
and HATENA_CONSUMER_SECRET must be defined in your settings.py.

ref : http://developer.hatena.ne.jp/ja/documents/auth/apis/oauth/consumer
"""
__author__ = 'giginet'
__version__ = '1.0.0'
__date__ = '2011/10/08'
import logging
logger = logging.getLogger(__name__)
logging.basicConfig()

from django.utils import simplejson
from social_auth.backends import ConsumerBasedOAuth, OAuthBackend, USERNAME, Token
from oauth2 import Request as OAuthRequest, SignatureMethod_HMAC_SHA1

# Hatena configuration
HATENA_SERVER = 'www.hatena.com'
HATENA_REQUEST_TOKEN_URL = 'https://%s/oauth/initiate' % HATENA_SERVER
HATENA_ACCESS_TOKEN_URL = 'https://%s/oauth/token' % HATENA_SERVER
HATENA_AUTHORIZATION_URL = 'https://www.hatena.ne.jp/oauth/authorize'
HATENA_CHECK_AUTH = 'http://n.hatena.com/applications/my.json'

class HatenaBackend(OAuthBackend):
    """Hatena OAuth authentication backend"""
    name = 'hatena'

    def get_user_details(self, response):
        """Return user details from Hatena account"""
        return {USERNAME: response['url_name'],
                'email': '',  # not supplied
                'fullname': response['display_name'],
                'first_name': '',
                'last_name': ''
        }
        
    def get_user_id(self, details, response):
        "OAuth providers return an unique user id in response"""
        return response['url_name']

class HatenaAuth(ConsumerBasedOAuth):
    """Hatena OAuth authentication mechanism"""
    AUTHORIZATION_URL = HATENA_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = HATENA_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = HATENA_ACCESS_TOKEN_URL
    SERVER_URL = HATENA_SERVER
    AUTH_BACKEND = HatenaBackend
    SCOPE_SEPARATOR = ','
    SETTINGS_KEY_NAME = 'HATENA_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'HATENA_CONSUMER_SECRET'
    
    def get_scope(self):
        return ('read_public',)

    def user_data(self, access_token):
        """Return user data provided"""
        request = self.oauth_request(access_token, HATENA_CHECK_AUTH)
        json = self.fetch_response(request)
        try:
            return simplejson.loads(json)
        except ValueError:
            return None
        
    def oauth_request(self, token, url, extra_params=None):
        scope = {'scope' : self.SCOPE_SEPARATOR.join(self.get_scope())}
        if not extra_params:
            extra_params = {}
        extra_params.update(scope)
        return super(HatenaAuth, self).oauth_request(token, url, extra_params)
        
    def access_token_request(self, token, url, extra_params=None):
        """Generate Access token request, setups callback url"""
        params = {}
        if extra_params:
            params.update(extra_params)

        if 'oauth_verifier' in self.data:
            params['oauth_verifier'] = self.data['oauth_verifier']
        request = OAuthRequest.from_consumer_and_token(self.consumer,
                                                       token=token,
                                                       http_url=url,
                                                       parameters=params)
        request.sign_request(SignatureMethod_HMAC_SHA1(), self.consumer, token)
        return request
    
    def access_token(self, token):
        """Return request for access token value"""
        request = self.access_token_request(token, self.ACCESS_TOKEN_URL)
        return Token.from_string(self.fetch_response(request))
    
# Backend definition
BACKENDS = {
    'hatena': HatenaAuth,
}
