# -*- coding: utf-8 -*-
#
# Author:        tohhy
# Date:          2011/11/04
#
from apps.categories.models import Category
from apps.materials.models import Material
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView


class SearchIndexView(ListView):
    model = Category
    template_name='index2.html'


class SearchResultView(ListView):
    model = Material
    template_name='searches/search_result.html'
    
    def get_context_data(self, **kwargs):
        category_id    = self.request.GET.get('category_id', None)
        search_keyword = self.request.GET.get('search_keyword', None)
        object_list = Material.objects
        print kwargs
        context = super(SearchResultView, self).get_context_data(**kwargs)
        if category_id:
            object_list = object_list.filter(category=Category.objects.get(id=category_id))
        if search_keyword:
            object_list = object_list.filter(label__contains=search_keyword)

        
        context['object_list'] = object_list
        context['category_list'] = Category.objects.all()
        return context
    
