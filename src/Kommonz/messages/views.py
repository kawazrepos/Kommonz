from django.template.context import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from auth.models import KommonzUser
from forms import MessageCreateForm
from models import Message
from object_permission.decorators import permission_required
import os


class MessageListView(ListView):
    model = Message
    
    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        inbox_object_list = Message.objects.filter(user_to=self.request.user)
        outbox_object_list = Message.objects.filter(user_from=self.request.user)
        context['inbox_object_list'] = inbox_object_list
        context['outbox_object_list'] = outbox_object_list
        return context


class MessageDetailView(DetailView):
    model = Message
    
    @method_decorator(permission_required('messages.view_message', Message))
    def dispatch(self, request, *args, **kwargs):
        message = Message.objects.get(pk=kwargs['pk'])
        if request.user == message.user_to and not message.read :
            message.read = True
            message.save()
        return super(MessageDetailView, self).dispatch(request, *args, **kwargs)


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm

    def post(self, request, *args, **kwargs):
        post_dict = request.POST.copy()
        users_to = post_dict.getlist('users_to')
        del post_dict["users_to"]
        create_object_dict = {"label" : post_dict['label'], "body" : post_dict['body'], 'user_from' : request.user}
        
        for userid in users_to:
            dict_copy = create_object_dict.copy()
            dict_copy['user_to'] = KommonzUser.objects.get(pk=userid)
            message = Message.objects.create(**dict_copy)
            message.save()
        return super(MessageCreateView, self).get(request, *args, **post_dict)


# create a fixed pattern message to user_to
# by messages/template_messages/template_filename
# usage: create_template_message(KommonzUser.objects.get(pk=1), 'welcome.txt')
def create_template_message(user_to, template_filename):
    template_path = os.path.join("messages/template_messages", template_filename)
    template = get_template(template_path)
    if template:
        create_object_dict = {'user_from' : KommonzUser.objects.get(pk=1),
                              'user_to' : user_to}
        context = Context(create_object_dict.copy())
        if len(template.nodelist):
            for block in template.nodelist:
                if isinstance(block, BlockNode) and block.name == 'label':
                    create_object_dict.update({'label' : block.render(context)})
                if isinstance(block, BlockNode) and block.name == 'body':
                    create_object_dict.update({'body' : block.render(context)})
            message = Message.objects.create(**create_object_dict)
            message.save()

