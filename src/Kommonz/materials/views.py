from django.views.generic import CreateView, DetailView
from models.base import Material
from forms import MaterialForm

class MaterialDetailView(DetailView):
    model = Material
    def get_context_data(self, **kwargs):
        context=super(DetailView, self).get_context_data(**kwargs)
        return context

class MaterialCreateView(CreateView):
    model = Material
    def get_form_class(self):
        return MaterialForm

    def get(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).post(request, *args, **kwargs)
