# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import render_to_response
from models import List, ListInfo
from utils.decorators import view_class_decorator
from apps.materials.models import Material

class ListDetailView(DetailView):
    model = List

class ListListView(ListView):
    model = List

@view_class_decorator(login_required)
class ListCreateView(CreateView):
    model = List

@view_class_decorator(login_required)
class ListAddView(UpdateView):
    model = List

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        material = request.POST.get('material', None)
        comment = request.POST.get('comment', '')
        info = ListInfo.objects.create(
            list=self.object,
            material=material,
            comment=comment
        )
        return super(ListAddlView, self).post(request, *args, **kwargs)

@view_class_decorator(login_required)
class ListRemoveView(UpdateView):
    model = List

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        material_pks = request.POST.get('materials', [])
        materials = [Material.objects.get(pk=pk) for pk in material_pks]
        for material in materials:
            list.materials.remove(material)
            info = ListInfo.objects.get(material=material, list=self.object)
        return super(ListAddlView, self).post(request, *args, **kwargs)

@view_class_decorator(login_required)
class ListDeleteView(DeleteView):
    model = List
