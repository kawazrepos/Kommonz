from apps.categories.models import Category
from django.views.generic.list import ListView


class CategoryListView(ListView):
    model = Category
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        target = Category.objects.get(pk=2)
        test_object_list = Category.objects.get_children(target).iterator()
        context['object_list'] = test_object_list
        return context