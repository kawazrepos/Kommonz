from django.views.generic.list import ListView
from object_permission.decorators import permission_required
from massages.models import Massage


class MassageListView(ListView):
    model = Massage
    
    def get_context_data(self, **kwargs):
        context = super(MassageListView, self).get_context_data(**kwargs)
        inbox_object_list = Massage.objects.all().filter(user_to=self.request.user)
        outbox_object_list = Massage.objects.all().filter(user_from=self.request.user)
        context['inbox_object_list'] = inbox_object_list
        context['outbox_object_list'] = outbox_object_list
        return context

    @permission_required('Kommonz.view_massage', Massage)
    def get(self, request, *args, **kwargs):
        return ListView.get(self, request, *args, **kwargs)
    