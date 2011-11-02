from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from auth.models import UserProfile
from forms import UserProfileUpdateForm


class UserProfileDetailView(DetailView):
    model = UserProfile


class UserProfileUpdateView(UpdateView):
    model       = UserProfile
    form_class  = UserProfileUpdateForm
    
    def get_queryset(self):
        self.kwargs.update({'slug' : self.request.user.profile.slug})
        return super(UserProfileUpdateView, self).get_queryset()
