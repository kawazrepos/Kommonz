# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from models import Report
from apps.reports.forms import ReportCreateForm


class ReportCreateView(CreateView):
    model = Report
    form_class = ReportCreateForm
