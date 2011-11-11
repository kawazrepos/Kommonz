from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from object_permission.decorators import permission_required
from models import Notification

class NotificationListView(ListView):
    model = Notification


class NotificationDetailView(DetailView):
    model = Notification
    
    @method_decorator(permission_required('apps.notifications.view_notification', Notification))
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationDetailView, self).dispatch(request, *args, **kwargs)
