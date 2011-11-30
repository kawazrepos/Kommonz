# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from object_permission.decorators import permission_required
from utils.decorators import view_class_decorator
from apps.materials.models import Material
from models import List, ListInfo

@view_class_decorator(permission_required('lists.view_list', List))
class ListDetailView(DetailView):
    """
    A View for list detail page.
    """
    model = List

@view_class_decorator(login_required)
class ListListView(ListView):
    """
    A View for own 'lists' list page.
    """
    model = List

    def get_queryset(self):
        qs = super(ListListView, self).get_queryset()
        return qs.filter(author=self.request.user)

@view_class_decorator(login_required)
class ListCreateView(CreateView):
    """
    A View for list creation.
    """
    model = List

@view_class_decorator(permission_required('lists.change_list', List))
class ListAddView(UpdateView):
    """
    A View for adding material to list.
    Post :
        material : a pk of adding material.
        comment  : comment.
    """
    model = List

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            material = Material.objects.get(pk=request.POST.get('material', None))
            comment = request.POST.get('comment', '')
            info = ListInfo.objects.create(
                list=self.object,
                material=material,
                comment=comment
            )
        except:
            pass
        return super(ListAddView, self).post(request, *args, **kwargs)

@view_class_decorator(permission_required('lists.change_list', List))
class ListRemoveView(UpdateView):
    """
    A View for removing materials from list.
    Post :
        materials : a tuple contains pks of removing materials.
    """
    model = List

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        material_pks = request.POST.get('materials', [])
        materials = [Material.objects.get(pk=pk) for pk in material_pks]
        for material in materials:
            info = ListInfo.objects.get(material=material, list=self.object)
            info.delete()
        return super(ListRemoveView, self).post(request, *args, **kwargs)

@view_class_decorator(permission_required('lists.change_list', List))
class ListUpdateView(UpdateView):
    """
    A View for list updating.
    """
    model = List

@view_class_decorator(permission_required('lists.delete_list', List))
class ListDeleteView(DeleteView):
    """
    A View for list deletion.
    """
    model = List

    def get_success_url(self):
        return reverse('lists_list_list')
