from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from models import Kero

class KeroListView(ListView):
    model = Kero
    
class KeroDetailView(DetailView):
    model = Kero
    