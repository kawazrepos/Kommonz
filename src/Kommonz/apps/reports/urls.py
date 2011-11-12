from apps.reports.views import ReportCreateView
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^create/?$',    ReportCreateView.as_view(), name='reports_report_create'),
)
