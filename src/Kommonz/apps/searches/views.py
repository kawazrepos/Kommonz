# -*- coding: utf-8 -*-
#
# Author:        tohhy
# Date:          2011/11/04
#
from apps.categories.models import Category
from apps.materials.models.base import Material
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView


class SearchIndexView(ListView):
    model=Category
    


class SearchResultView(ListView):
    model = Material
    
    def get_context_data(self, **kwargs):
        category_id = self.request.GET.get('category_id', None)
        print kwargs
        context = super(SearchResultView, self).get_context_data(**kwargs)
        if category_id:
            print "ok"
            object_list = Material.objects.filter(category=Category.objects.get(id=category_id))
            context['object_list'] = object_list
            
        return context
    