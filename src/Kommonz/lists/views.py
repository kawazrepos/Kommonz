# Create your views here.
from django.views.generic import TemplateView
from lists.models import List
from lists.models import ListInfo
from django.views.generic import CreateView, DetailView
from materials.models.base import Material
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
