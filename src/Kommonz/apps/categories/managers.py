# -*- coding: utf-8 -*-
from django.db import models


class CategoryManager(models.Manager):
    
    def get_child_categories(self, instance):
        results = self.filter(pk=1)
        return results