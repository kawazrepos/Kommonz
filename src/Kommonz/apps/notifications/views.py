from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from object_permission.decorators import permission_required
from models import Notification

class NotificationListView(ListView):
    model = Notification


@permission_required('apps.notifications.view_notification')
class NotificationDetailView(DetailView):
    model = Notification
