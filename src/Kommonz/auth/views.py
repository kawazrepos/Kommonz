from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from forms import UserUpdateForm, UserProfileUpdateForm, UserOptionUpdateForm
from models import UserProfile, UserOption


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
