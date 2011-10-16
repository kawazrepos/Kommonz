from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from Kommonz.massages.models import Massage

class MassageCreateView(CreateView):
    model = Massage

    def get(self, request, *args, **kwargs):
        return super(MassageCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post = super(MassageCreateView, self).post(request, *args, **kwargs)
        post['user_from'] = self.request.user
        return post

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