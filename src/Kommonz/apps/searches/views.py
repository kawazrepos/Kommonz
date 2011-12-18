# -*- coding: utf-8 -*-
#
# Author:        giginet
# Modifier:      tohhy
# Date:          2011/11/04
#
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.list import ListView

from apps.categories.models import Category
from apps.materials.models import Material
from forms import ExtendSearchForm, SORTS

class SearchResultView(ListView):
    """
    A View for search result.
    """
    model = Material
    template_name = 'searches/search_result.html'
    
    def get_queryset(self):
        """
        Get filtered queryset by GET parameters.
        """
        qs = super(SearchResultView, self).get_queryset()
        params = dict(self.request.GET.copy())
        queries = []
        if 'q' in params:
            q = params['q'][0]
            queries.append(Q(label__contains=q))
            queries.append(Q(description__contains=q))
        if 'category' in params:
            try:
                category = Category.objects.get(pk=params['category'][0])
                not_matched_categories = Category.objects.exclude(pk=category.pk)
                children = Category.objects.get_children(category)
                for child in children:
                    not_matched_categories = not_matched_categories.exclude(pk=child.pk)
                for not_matched_category in not_matched_categories:
                    qs = qs.exclude(category=not_matched_category)
            except:
                pass
        if queries:
            query = reduce(lambda a, b : a | b, queries)
            qs = qs.filter(query)
        if 'order' in params and 'sort' in params and params['sort'][0] in dict(SORTS):
            sort = params['sort'][0]
            if 'order' == 'd':
                sort = '-%s' % sort
            qs = qs.order_by(sort)
        return qs


    def get_context_data(self, **kwargs):
        """
        Add ExtendSearchForm instance to context.
        """
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context['form'] = ExtendSearchForm(self.request.GET.get('q', ''))
        limit = self.request.GET.get('limit', '20')
        limit = int(limit) if limit.isdigit() else 20
        paginator = Paginator(context['object_list'], limit)
        n = self.request.GET.get('n', '1')
        context['object_list'] = paginator.page(n).object_list
        context['paginator'] = paginator
        context['query'] = self.request.GET.get('q', '')
        return context
