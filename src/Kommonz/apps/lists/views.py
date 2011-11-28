# Create your views here.
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.shortcuts import render_to_response
from models import List, ListInfo
from apps.materials.models import Material

class ListDetailView(DetailView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(ListDetailView, self).get_context_data(**kwargs)
        print context.__dict__
        List_ordered_by_add_at(context.object)
        context['ordered_list'] = List_ordered_by_add_at(context.object)
        return context

class ListListView(ListView):
    model = List
    def get_context_data(self, **kwargs):
        context = super(ListListView, self).get_context_data(**kwargs)
        return context

def List_ordered_by_add_at(instance):
    order = instance.order
    sorting = ""
    if order == 'listinfo__add_date':
        sorting = "listinfo__add_date"
    elif order == 'downloads_times':
        sorting = 'downloads_times'
    elif order == 'material_upload_date':
        sorting = 'material_upload_date'
    elif order == 'author':
        sorting = 'author'
    elif order == '-listinfo__add_date':
        sorting = '-listinfo__add_date'
    elif order == '-download_times':
        sorting = '-download_times'
    elif order == '-material_upload_date':
        sorting = '-material_upload_date'
    else: 
        sorting = '-author'
        
    ordered_list = List.objects.all().order_by(sorting)
    return ordered_list
