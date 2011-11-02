# Create your views here.
from django.views.generic import TemplateView
from lists.model import List
from lists.model import ListInfo
from django.views.generic import CreateView, DetailView
from models.base import Material
from forms import MaterialForm

class ListDetailView(DetailView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context

class ListListView(ListView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        return context
