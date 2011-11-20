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
        object_list    = Material.objects.order_by() # empty ordering to make fast
        context        = super(SearchResultView, self).get_context_data(**kwargs)
        
        # matches
        category_id    = self.request.GET.get('category_id', None)
        search_keyword = self.request.GET.get('search_keyword', None)
        
        # display ways
        display_number = self.request.GET.get('display_number', None)
        page_number    = self.request.GET.get('page_number', None)
        sort           = self.request.GET.get('sort', None)
        order          = self.request.GET.get('order', None)
        
        # thresholds
        # usage:
        # searches/?download_number=500o
        # over 500 downloads will be displayed
        # searches/?download_number=500b
        # below 500 downloads will be displayed
        
        image_size      = self.request.GET.get('image_size', None)
        audio_length    = self.request.GET.get('audio_length', None)
        download_number = self.request.GET.get('download_number', None)
        
        
        # making query
        if category_id:
            try:
                category=Category.objects.get(id=category_id)
                object_list = object_list.filter(category=category)
            except Category.DoesNotExist:
                pass
                
        if search_keyword:
            object_list = object_list.filter(label__contains=search_keyword)
            
        if isinstance(download_number, basestring):
            tail = ''
            if download_number[-1] == u'o':
                download_number = download_number[:-1]
                tail = 'o'
            elif download_number[-1] == u'b':
                download_number = download_number[:-1]
                tail = 'b'
            print download_number + ':' + str(download_number.isdigit())
            
            if download_number.isdigit():
                if tail == 'b':
                    object_list = object_list.filter(download__lte=int(download_number))
                else:
                    object_list = object_list.filter(download__gte=int(download_number))
            
        
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