# Create your views here.
from Kommonz.materials.models.base import Material
from django.views.generic.detail import DetailView

class MaterialDetailView(DetailView):
    template_name = 'detail.html'
    model=Material
    def get_context_data(self, **kwargs):
        context=super(DetailView, self).get_context_data(**kwargs)
        return context