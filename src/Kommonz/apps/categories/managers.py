# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

class CategoryManager(models.Manager):
    def get_children(self, category):
        from models import Category
        if category.children.count() is 0: return self.none()
        def _get_set(category):
            categories = set([category,])
            for child in category.children.iterator():
                categories.update(_get_set(child)) 
            return categories
        queries = [Q(parent=category) for category in _get_set(category)]
        query = reduce(lambda a, b : a | b, queries)
        return Category.objects.filter(query)
    
#    def get_parents(self, instance):
#        results = instance.parent
#        if instance.parent:
#            if instance.parent.parent:
#                for p in self.get_parents(instance.parent).iterator():
#                    results.add(p)    
#        return results
#    
