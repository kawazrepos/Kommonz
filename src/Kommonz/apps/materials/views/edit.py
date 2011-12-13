from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from utils.views import JSONResponse
from utils.decorators import view_class_decorator

from apps.categories.models import Category

from ..models import Material, MaterialFile
from ..forms import MaterialFileForm, MaterialUpdateForm
from ..api.mappers import MaterialFileMapper
from ..utils.filetypes import guess

def response_mimetype(request):
    if request.META.has_key('HTTP_ACCEPT') and "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"

def set_material_model(func):
    def _decorator(self, request, *args, **kwargs):
        if request.META['REQUEST_METHOD'] == 'GET':
            self.filename = request.GET.get('filename', None)
        elif request.META['REQUEST_METHOD'] == 'POST':
            try:
                file_pk = request.POST.get('_file', None)
                file = MaterialFile.objects.get(pk=file_pk)
                self.filename = file.file.name
            except:
                pass
        self.material_model = Material.objects.get_file_model(self.filename)
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
        category = Category.objects.get_filetype_category(self.filename)
        modelform_class = type('modelform', (forms.ModelForm,), {
            "Meta": meta, 
            "_file" : filefield, 
            "label.initial" : self.filename, 
            "category" : forms.ModelChoiceField(queryset=Category.objects.all(), initial=category)
        }) # create new class extended MaterialUpdateForm
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

@view_class_decorator(login_required)
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

#@view_class_decorator(permission_required('materials.change_material', Material))
class MaterialUpdateView(UpdateView):
    template_name = 'materials/material_update_form.html'
    queryset      = Material.objects.all()

    def post(self, request, *args, **kwargs):
        f = request.FILES.pop('file', [])[0]
        self.object = self.get_object()
        if f:
            old_type = guess(self.get_object().file.name)
            new_type = guess(f.name)
            if not old_type == new_type:
                form = self.get_form_class()(**self.get_form_kwargs())
                form.errors.update({'file' : [_('Material filetype must be same between old and new file.'), ]})
                return self.render_to_response(self.get_context_data(form=form))
            material_file = self.object._file
            material_file.file = f
            material_file.save()
        return super(MaterialUpdateView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(MaterialUpdateView, self).get_form_kwargs()
        kwargs.update({'material' : self.object})
        return kwargs

    def get_form_class(self):
        return MaterialUpdateForm
