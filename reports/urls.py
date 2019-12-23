from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from reports.views import ReportView

urlpatterns = [
    url(r'^$', ReportView.as_view(), name='get_xlsx_reports'),
    url(r'^data_export$', 'reports.views.data_export', name='get_data_export'),
]
