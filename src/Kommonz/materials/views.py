from django.views.generic import CreateView, DetailView
from django.http import HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse

from django.conf import settings

from models.base import Material
from forms import MaterialForm

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
        f = self.request.FILES.get('file')
        
        data = [{'label': f.name, 'url': settings.MEDIA_URL + "pictures/" + f.name, 'thumbnail_url': settings.MEDIA_URL + "pictures/" + f.name, 'delete_url': '', 'delete_type': "DELETE"}]
        
        response = JSONResponse(data, {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_form_class(self):
        return MaterialForm

    def get(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).post(request, *args, **kwargs)

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self,obj='',json_opts={}, mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj,**json_opts)
        print content
        super(JSONResponse,self).__init__(content, mimetype, *args, **kwargs)
