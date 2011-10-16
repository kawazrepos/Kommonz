# -*- coding: utf-8 -*-
from Kommonz.reports.models import Report
from django.views.generic.edit import CreateView
class ReportCreateView(CreateView):
    model = Report

    def get(self, request, *args, **kwargs):
        return super(ReportCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(ReportCreateView, self).post(request, *args, **kwargs)
