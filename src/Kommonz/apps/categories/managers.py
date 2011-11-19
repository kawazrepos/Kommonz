# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q

class CategoryManager(models.Manager):
    
    def get_children_tree(self, category):
        def _get_dict(category):
            child_categories = {}
            for child in category.children.iterator():
                child_categories.update({child.label : _get_dict(child)})
            return child_categories
        result = _get_dict(category)
        return result
        
    
    def get_filetype_category(self, filename):
        from django.contrib.contenttypes.models import ContentType
        from django.core.exceptions import ObjectDoesNotExist
        from apps.materials.utils import filetypes
        from models import Category
        model = filetypes.get_file_model(filename)
        model_ct = ContentType.objects.get_for_model(model)
        try:
            category = Category.objects.get(Q(label=model_ct.name),
                                            Q(parent=None))
            return category
        except ObjectDoesNotExist:
            category = Category.objects.create(label=model_ct.name)
            return category

    
    def get_children(self, category):
        from models import Category
        def _get_set(category):
            categories = set([category,])
            for child in category.children.iterator():
                categories.update(_get_set(child)) 
            return categories
        queries = [Q(parent=category) for category in _get_set(category)]
        query = reduce(lambda a, b : a | b, queries)
        return Category.objects.filter(query)
    
    
    def get_parents(self, category):
        from models import Category
        def _get_set(category):
            categories = set([category,])
            if category.parent:
                categories.update(_get_set(category.parent))
            return categories
        categories = _get_set(category)
        categories.remove(category)
        queries = [Q(pk=category.pk) for category in categories]
        query = reduce(lambda a, b : a | b, queries, Q(pk=None))
        return Category.objects.filter(query)
    
