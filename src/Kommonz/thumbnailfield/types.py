# -*- coding: utf-8 -*-
#
# src/Kommonz/thumbnailfield/types.py
# created by giginet on 2011/10/13
#


class Thumbnail(object):
    def __init__(self, sizes=()):
        for size, thumbnail in sizes:
            setattr(self, size, thumbnail)

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return "thumbnail"
