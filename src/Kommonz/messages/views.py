from auth.models import KommonzUser
from django.template.context import Context
from django.template.loader import get_template, get_template_from_string
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from messages.forms import MessageCreateForm
from messages.models import Message
from object_permission.decorators import permission_required


class MessageListView(ListView):
    model = Message
    
    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        inbox_object_list = Message.objects.all().filter(user_to=self.request.user)
        outbox_object_list = Message.objects.all().filter(user_from=self.request.user)
        context['inbox_object_list'] = inbox_object_list
        context['outbox_object_list'] = outbox_object_list
        return context


class MessageDetailView(DetailView):
    model = Message
    
    @method_decorator(permission_required('messages.view_message', Message))
    def dispatch(self, request, *args, **kwargs):
        message = Message.objects.get(pk=kwargs['pk'])
        if not message.read:
            message.read = True
            message.save()
        return DetailView.dispatch(self, request, *args, **kwargs)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm

    def post(self, request, *args, **kwargs):
        dict = request.POST.copy()
        users_to = dict.getlist('users_to')
        del dict["users_to"]
        create_object_dict = {"label" : dict['label'], "body" : dict['body'], 'user_from' : request.user}
        
        for userid in users_to:
            dict_copy = create_object_dict.copy()
            dict_copy['user_to'] = KommonzUser.objects.get(pk=userid)
            message = Message.objects.create(**dict_copy)
            message.save()
        
        return CreateView.get(self, request, *args, **dict)


def create_template_message(user_to, template_filename):
    template_path = "messages/template_messages/" + template_filename
    template = get_template(template_path)
    if template:
        create_object_dict = {'user_from' : KommonzUser.objects.get(pk=1),
                              'user_to' : user_to}
        context = Context(create_object_dict.copy())
        label_loader = get_template_from_string('{% extends "' + template_path + '" %}{% block label %}{% endblock %}')
        body_loader = get_template_from_string('{% extends "' + template_path + '" %}{% block body %}{% endblock %}')
        create_object_dict.update({'label' : label_loader.render(context), 'body' : body_loader.render(context)})
        message = Message.objects.create(**create_object_dict)
        message.save()

