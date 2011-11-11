from django.views.generic.base import TemplateView


class ControlView(TemplateView):
    template_name = "control/control_main.html"
