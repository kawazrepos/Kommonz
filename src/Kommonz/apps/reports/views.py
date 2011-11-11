# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from models import Report
class ReportCreateView(CreateView):
    model = Report

    def get(self, request, *args, **kwargs):
        return super(ReportCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(ReportCreateView, self).post(request, *args, **kwargs)
