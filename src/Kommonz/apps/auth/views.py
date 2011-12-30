from django.contrib.auth.models import User
from django.utils.decorators import classonlymethod
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from forms import UserUpdateForm, UserProfileUpdateForm, UserOptionUpdateForm
from models import UserProfile, UserOption
from social_auth.models import UserSocialAuth


class UserMaterialListView(DetailView):
    model = User
    template_name = "auth/user_material_list.html"

class UserProfileDetailView(DetailView):
    model = UserProfile

class UserUpdateView(UpdateView):
    model       = User
    form_class  = UserUpdateForm
    
    def get_queryset(self):
        self.kwargs.update({'pk' : self.request.user.pk})
        return super(UserUpdateView, self).get_queryset()


class UserProfileUpdateView(UpdateView):
    model       = UserProfile
    form_class  = UserProfileUpdateForm
    
    def get_queryset(self):
        self.kwargs.update({'pk' : self.request.user.pk})
        return super(UserProfileUpdateView, self).get_queryset()


class UserOptionUpdateView(UpdateView):
    model       = UserOption
    form_class  = UserOptionUpdateForm
    
    def get_queryset(self):
        self.kwargs.update({'pk' : self.request.user.pk})
        return super(UserOptionUpdateView, self).get_queryset()
    
    
class UserAccountUpdateView(TemplateView):
    template_name = "auth/useraccount_form.html"
    
    def get_context_data(self, **kwargs):
        context = super(UserAccountUpdateView, self).get_context_data(**kwargs)
        context.update({'associated_accounts' : UserSocialAuth.objects.filter(user=self.request.user)})
        return context
    
