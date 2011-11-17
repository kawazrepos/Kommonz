# -*- coding: utf-8 -*-
#
# src/Kommonz/apps/materials/querysets.py
# created by giginet on 2011/11/17
#
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

class SubclassingQuerySet(QuerySet):
    def __getitem__(self, k):
        result = super(SubclassingQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result
    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()

