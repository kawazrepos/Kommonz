# Create your views here.
from Kommonz.auth.models import KommonzUser
from django.views.generic.detail import DetailView

class UserDetailView(DetailView):
    template_name = 'detail.html'
    model=KommonzUser
    def get_context_data(self, **kwargs):
        context=super(DetailView, self).get_context_data(**kwargs)
        return context