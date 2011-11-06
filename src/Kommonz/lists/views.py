# Create your views here.
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from lists.models import List, ListInfo
from materials.models.base import Material


class ListDetailView(DetailView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(ListDetailView, self).get_context_data(**kwargs)
        return context
    

class ListListView(ListView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(ListListView, self).get_context_data(**kwargs)
        return context
