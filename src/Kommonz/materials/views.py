from django.views.generic import CreateView, DetailView, UpdateView
from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings

from models.base import Material
from forms import MaterialForm, MaterialExtendForm
from api.mappers import MaterialMapper


class MaterialDetailView(DetailView):
    model = Material
    
    def get_context_data(self, **kwargs):
        context=super(DetailView, self).get_context_data(**kwargs)
        return context

def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

class MaterialCreateView(CreateView):
    model = Material
    template_name = 'materials/material_form.html'
   
    def form_valid(self, form):
        self.object = form.save()
        
        mapper = MaterialMapper(self.object)
        
        response = JSONResponse([mapper.as_dict(),], {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_form_class(self):
        return MaterialForm

    def get(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).post(request, *args, **kwargs)

class MaterialExtendFormView(UpdateView):
    template_name = 'materials/material_extend_form.html'
    queryset      = Material.objects.all()
    
    def get(self, request, *args, **kwargs):
        from utils.filetypes import get_file_class
        pk = kwargs.get('pk')
        instance = Material.objects.get(pk=pk)
        self.model = get_file_class(instance.file.name)
        return super(MaterialExtendFormView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        from utils.filetypes import get_file_class
        pk = kwargs.get('pk')
        instance = Material.objects.get(pk=pk)
        self.model = get_file_class(instance.file.name)
        return super(MaterialExtendFormView, self).get(request, *args, **kwargs)
    
    def get_form_class(self):
        # ref http://www.agmweb.ca/blog/andy/2249/
        meta = type('Meta', (), { "model" : self.model, "exclude" : 'file', }) # create Meta class(ref Expert Python Programming p119)
        modelform_class = type('modelform', (MaterialExtendForm,), {"Meta": meta}) # create new class extend MaterialExtendForm
        return modelform_class

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
