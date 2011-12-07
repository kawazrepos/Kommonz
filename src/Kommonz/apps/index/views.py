from django.views.generic.base import TemplateView
from apps.materials.models import Material
from apps.searches.forms import SearchForm

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['latest_materials'] = Material.objects.order_by('-created_at')[:5]
        context['form'] = SearchForm()
        return context
