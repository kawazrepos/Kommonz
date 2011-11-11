# Create your views here.
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.shortcuts import render_to_response
from lists.models import List, ListInfo
from materials.models.base import Material


class ListDetailView(DetailView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(ListDetailView, self).get_context_data(**kwargs)
        print object
        return context


class ListListView(ListView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(ListListView, self).get_context_data(**kwargs)
        return context

def List_ordered_by_add_at(request):
    ordered_list = List.objects.all().order_by('-created_at')
    return render_to_response('lists/list_list.html', {'object_list': ordered_list})
