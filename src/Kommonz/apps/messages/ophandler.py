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

from object_permission import site
from object_permission.handlers import ObjectPermHandler

from models import Message

class MessageObjectPermHandler(ObjectPermHandler):

    def setup(self):
        self.watch('user_to')
        self.watch('user_from')
        self.watch('pub_state')

    def updated(self, attr):
        self.reject(None)
        self.reject('anonymous')
        if self.instance.pub_state == 'sent':
            self.viewer(self.instance.user_to)
            self.viewer(self.instance.user_from)
            self.reject(None)
            self.reject('anonymous')
        elif self.instance.pub_state == 'deleted':
            self.reject(self.instance.user_to)
            self.reject(self.instance.user_from)
        elif self.instance.pub_state == 'receiver_deleted':
            self.reject(self.instance.user_to)
            self.viewer(self.instance.user_from)
        elif self.instance.pub_state == 'sender_deleted':
            self.viewer(self.instance.user_to)
            self.reject(self.instance.user_from)
            
site.register(Message, MessageObjectPermHandler)
