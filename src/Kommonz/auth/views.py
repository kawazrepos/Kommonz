from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from forms import UserUpdateForm
from models import User

class UserDetailView(DetailView):
    model = User


class UserUpdateView(UpdateView):
    model       = User
    form_class  = UserUpdateForm
    
    def get_queryset(self):
        self.kwargs.update({'pk' : self.request.user.pk})
        return super(UserUpdateView, self).get_queryset()

