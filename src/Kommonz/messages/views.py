import os
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.context import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from object_permission.decorators import permission_required
from auth.models import User
from materials.models.base import Material
from forms import MessageCreateForm, MaterialMessageCreateForm, \
                  ReplyMessageCreateForm, MessageDeleteForm
from models import Message


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
    
    def get(self, request, *args, **kwargs):
        if request.GET.get('pk', None):
            if request.GET.get('message_type', None) == 'material_message':
                self.form_class = MaterialMessageCreateForm
                material = Material.objects.get(pk=request.GET.get('pk'))
                # if collabolators implemented, edit below
                self.initial.update({'users_to' : (material.author.pk,)})
            elif request.GET.get('message_type', None) == 'reply':
                self.form_class = ReplyMessageCreateForm
                self.initial.update({'users_to' : (request.GET.get('pk'),)})
        else:
            self.form_class = MessageCreateForm
        return super(MessageCreateView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        post_dict = request.POST.copy()
        users_to = self.initial.get('users_to', None)
        if not users_to:
            users_to = post_dict.getlist('users_to')
        if post_dict.get('users_to', None):
            del post_dict['users_to']
        
        if users_to:
            for userid in users_to:
                create_object_dict = {'label' : post_dict['label'], 'body' : post_dict['body'],
                                  'user_from' : request.user, 'pub_state' : 'sent'}
                create_object_dict['user_to'] = User.objects.get(pk=userid)
                message = Message.objects.create(**create_object_dict)
                message.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(MessageCreateView, self).post(request, *args, **kwargs)
        
    def get_success_url(self):
        return reverse('messages_message_outbox')


class MessageDeleteView(UpdateView):
    model = Message
    form_class = MessageDeleteForm
    
    def get_success_url(self):
        return reverse('messages_message_list')
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.request.user == self.object.user_to:
            if self.object.pub_state == 'sender_deleted':
                self.object.pub_state = 'deleted'
            else:
                self.object.pub_state = 'receiver_deleted'
            self.object.save()
        
        elif self.request.user == self.object.user_from:
            if self.object.pub_state == 'receiver_deleted':
                self.object.pub_state = 'deleted'
            else:
                self.object.pub_state = 'sender_deleted'
            self.object.save()
        
        return HttpResponseRedirect(self.get_success_url())
    

# create a fixed pattern message to user_to
# by messages/template_messages/template_filename
# usage: create_template_message(User.objects.get(pk=1), 'welcome.txt')
def create_template_message(user_to, template_filename):
    template_path = os.path.join('messages/template_messages', template_filename)
    template = get_template(template_path)
    if template:
        create_object_dict = {'user_from' : User.objects.get(pk=1),
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

