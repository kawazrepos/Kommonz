# -*- coding: utf-8 -*-
import copy
from django.db import models


class CategoryManager(models.Manager):
    
    def get_children(self, instance):
        children = instance.children
        results = copy.copy(children)
        for child in children.iterator():
            results.add(child) 
            if child.children.count() > 0:
                self.get_children(child)
                    
        return results
    
#    def get_parents(self, instance):
#        results = instance.parent
#        if instance.parent:
#            if instance.parent.parent:
#                for p in self.get_parents(instance.parent).iterator():
#                    results.add(p)    
#        return results
#    