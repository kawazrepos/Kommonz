from apps.categories.models import Category
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class CategoryListView(ListView):
    model = Category
    
class CategoryDetailView(DetailView):
    model = Category
    