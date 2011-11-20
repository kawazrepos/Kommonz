# -*- coding: utf-8 -*-
#
# Author:        tohhy
# Date:          2011/11/04
#
from django.core.paginator import Paginator
from django.views.generic.list import ListView

from apps.categories.models import Category
from apps.materials.models import Material


class SearchIndexView(ListView):
    model = Category
    template_name='index2.html'
    

class SearchResultView(ListView):
    model = Material
    template_name='searches/search_result.html'
    
    def get_context_data(self, **kwargs):
        category_id    = self.request.GET.get('category_id', None)
        search_keyword = self.request.GET.get('search_keyword', None)
        display_number = self.request.GET.get('display_number', None)
        page_number    = self.request.GET.get('page_number', None)
        sort           = self.request.GET.get('sort', None)
        order          = self.request.GET.get('order', None)
        object_list    = Material.objects.order_by() # empty ordering to make fast
        context        = super(SearchResultView, self).get_context_data(**kwargs)
        
        # making query
        if category_id:
            try:
                category=Category.objects.get(id=category_id)
                object_list = object_list.filter(category=category)
            except Category.DoesNotExist:
                pass
                
        if search_keyword:
            object_list = object_list.filter(label__contains=search_keyword)
            
        # ordering
        object_list = self._get_ordered_object_list(object_list, sort, order)
                
        # display and paginate
        if not isinstance(display_number, basestring) or not display_number.isdigit():
            display_number = 3
        else:
            display_number = int(display_number)
        paginator = Paginator(object_list, display_number)
        
        if not isinstance(page_number, basestring) or not page_number.isdigit():
            page_number = 1
        else:
            page_number = int(page_number)
            if page_number > paginator.page_range[-1]:
                page_number = paginator.page_range[-1]

        # making context
        context['object_list'] = paginator.page(page_number).object_list
        context['category_list'] = Category.objects.all()
        return context
    
    
    def _get_ordered_object_list(self, object_list, sort, order):
        sorting = ""
        
        if sort == 'pv':
            sorting = 'pv'
        elif sort == 'download':
            sorting = 'download'
        elif sort == 'created_at':
            sorting = 'created_at'
        elif sort == 'updated_at':
            sorting = 'updated_at'
        else:
            sorting = 'pk'
            
        if order == 'd':
            sorting = '-' + sorting
        
        return object_list.order_by(sorting)