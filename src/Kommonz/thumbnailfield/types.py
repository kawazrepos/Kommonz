# -*- coding: utf-8 -*-
#
# src/Kommonz/thumbnailfield/types.py
# created by giginet on 2011/11/06
#
class Thumbnail(object):
    def __init__(self, thumbnail_pattern={}):
        for name, path in thumbnail_pattern:
            setattr(self, name, path)
