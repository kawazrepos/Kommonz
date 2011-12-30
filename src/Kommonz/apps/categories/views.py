from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from models import Category


class CategoryListView(ListView):
    model = Category
    
class CategoryDetailView(DetailView):
    model = Category
    