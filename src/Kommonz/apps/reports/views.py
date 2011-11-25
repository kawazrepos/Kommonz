# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from apps.materials.models import Material
from models import Report
from forms import ReportCreateForm


class ReportCreateView(CreateView):
    model = Report
    form_class = ReportCreateForm

