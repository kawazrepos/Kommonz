# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from models import List, ListInfo
from apps.materials.models import Material

class ListDetailView(DetailView):
    model = List

class ListListView(ListView):
    model = List

class ListCreateView(CreateView):
    model = List
    def form_valid(self, form):
        self.object = List.objects.create(
            label=form.cleaned_data.get('label', ''),
            author=self.request.user,
            pub_state=form.cleaned_data['pub_state'],
            order=form.cleaned_data['order'],
            description=form.cleaned_data.get('description', '')
        )
        for material in form.cleaned_data.get('materials', []):
            try:
                info = ListInfo.objects.create(
                    list=self.object,
                    material=Material.objects.get(pk=material)
                )
            except:
                pass
        return super(ModelFormMixin, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListCreateView, self).dispatch(*args, **kwargs)
