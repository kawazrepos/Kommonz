from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from notifications.models import Notification
from object_permission.decorators import permission_required


class NotificationListView(ListView):
    model = Notification


class NotificationDetailView(DetailView):
    model = Notification
    
    @method_decorator(permission_required('notifications.view_notification', Notification))
    def dispatch(self, request, *args, **kwargs):
        notification = Notification.objects.get(pk=kwargs['pk'])
        if request.user == notification.user_to and not notification.read :
            notification.read = True
            notification.save()
        return super(NotificationDetailView, self).dispatch(request, *args, **kwargs)


