from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from massages.models import Massage
from object_permission.decorators import permission_required


class MassageListView(ListView):
    model = Massage
    
    def get_context_data(self, **kwargs):
        context = super(MassageListView, self).get_context_data(**kwargs)
        inbox_object_list = Massage.objects.all().filter(user_to=self.request.user)
        outbox_object_list = Massage.objects.all().filter(user_from=self.request.user)
        context['inbox_object_list'] = inbox_object_list
        context['outbox_object_list'] = outbox_object_list
        return context


class MassageDetailView(DetailView):
    model = Massage
    
    @method_decorator(permission_required('massages.view_massage', Massage))
    def dispatch(self, request, *args, **kwargs):
        return DetailView.dispatch(self, request, *args, **kwargs)


class MassageCreateView(CreateView):
    model = Massage
