# Create your views here.
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from object_permission.decorators import permission_required
from utils.decorators import view_class_decorator
from apps.materials.models import Material
from apps.materials.views.zip import MaterialZipView
from models import List, ListInfo
from forms import ListOrderForm

@view_class_decorator(permission_required('lists.view_list', List))
class ListDetailView(DetailView):
    """
    A View for list detail page.
    """
    model = List

    def get_context_data(self, **kwargs):
        """
        Set materials as context.
        If the view recives 'order' as GET parameter, 
        materials will be ordered by that.
        And ListOrderForm instance as order_form
        """
        order = self.request.GET.get('order', None)
        context = super(ListDetailView, self).get_context_data(**kwargs)
        context['materials'] = self.object.materials
        from models import ORDER_STATES
        if order and order in dict(ORDER_STATES):
            context['materials'] = context['materials'].order_by(order)
        context['order_form'] = ListOrderForm()
        return context
        
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
class ListAddView(CreateView):
    """
    A View for adding material to list.
    Post :
        material : a pk of adding material.
        comment  : comment.
    """
    model = ListInfo

    def get(self, request, *args, **kwargs):
        get_object_or_404(List, pk=kwargs.get('pk'))
        return super(ListAddView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        list = get_object_or_404(List, pk=kwargs.get('pk'))
        post = request.POST.copy()
        post['list'] = kwargs['pk']
        request.POST = post
        print request.POST
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
        try:
            materials = [Material.objects.get(pk=pk) for pk in material_pks]
        except:
            materials = []
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

@view_class_decorator(permission_required('lists.view_list', List))
class ListZipView(MaterialZipView):
    def get(self, request, *args, **kwargs):
        self.list_pk = kwargs.pop('pk', None)
        return super(ListZipView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        list = get_object_or_404(List, pk=self.list_pk)
        if list:
            return list.materials
        return Material.objects.none()
