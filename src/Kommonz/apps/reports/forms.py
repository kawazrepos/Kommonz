from django.forms.models import ModelForm
from apps.reports.models import Report


class ReportCreateForm(ModelForm):
    
    class Meta:
        model = Report
        fields = ('reason', 'remarks',)
