from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django import forms

from object_permission.decorators import permission_required

from ..models import Material, MaterialFile
from ..forms import MaterialForm, MaterialFileForm
from ..api.mappers import MaterialMapper, MaterialFileMapper

def response_mimetype(request):
    if request.META.has_key('HTTP_ACCEPT') and "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

def set_material_model(func):
    def _decorator(self, request, *args, **kwargs):
        filename = None
        if request.META['REQUEST_METHOD'] == 'GET':
            filename = request.GET.get('filename', None)
        elif request.META['REQUEST_METHOD'] == 'POST':
            try:
                file_pk = request.POST.get('_file', None)
                file = MaterialFile.objects.get(pk=file_pk)
                filename = file.file.name
            except:
                pass
        self.material_model = Material.objects.get_file_model(filename)
        res = func(self, request, *args, **kwargs)
        return res
    return _decorator

class MaterialCreateView(CreateView):
    template_name = "materials/material_form.html"

    @set_material_model
    def get(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).get(request, *args, **kwargs)

    @set_material_model
    def post(self, request, *args, **kwargs):
        return super(MaterialCreateView, self).post(request, *args, **kwargs)

    def get_form_class(self):
        # ref http://www.agmweb.ca/blog/andy/2249/
        args = getattr(self, 'FORM_META_ARGS', {})
        args.update({'model' : self.material_model})
        meta = type('Meta', (), args) # create Meta class(ref Expert Python Programming p119)
        from django import forms
        filefield = forms.IntegerField(widget=forms.HiddenInput())
        modelform_class = type('modelform', (forms.ModelForm,), {"Meta": meta, "_file" : filefield}) # create new class extended MaterialUpdateForm
        return modelform_class

class MaterialValidateView(MaterialCreateView):
    def form_valid(self, form):
        response = {
                    'status' : 'success',
        }
        return JSONResponse(response, {}, response_mimetype(self.request))

    def form_invalid(self, form):
        response = {
                    'status' : 'error',
                    'errors' : form.errors,
        }
        return JSONResponse(response, {}, response_mimetype(self.request))

class MaterialFileCreateView(CreateView):
    model = MaterialFile
    template_name = 'materials/material_file_form.html'

    def form_valid(self, form):
        self.object = form.save()
        mapper = MaterialFileMapper(self.object)
        response = JSONResponse([mapper.as_dict(),], {}, response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def get_form_class(self):
        return MaterialFileForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MaterialFileCreateView, self).dispatch(*args, **kwargs)

class MaterialUpdateView(UpdateView):
    template_name = 'materials/material_update_form.html'
    queryset      = Material.objects.all()
    
    @method_decorator(permission_required('apps.materials.change_material', Material))
    def dispatch(self, *args, **kwargs):
        return super(MaterialUpdateView, self).dispatch(*args, **kwargs)

class MaterialInlineUpdateView(MaterialUpdateView):
    template_name = 'materials/material_inline_form.html'
    FORM_META_ARGS = {
                      'exclude' : 'file'
    }
    
    @method_decorator(csrf_exempt)    
    @method_decorator(permission_required('apps.materials.change_material', Material))
    def dispatch(self, *args, **kwargs):
        return super(MaterialUpdateView, self).dispatch(*args, **kwargs)

class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts={}, mimetype="application/json", *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
