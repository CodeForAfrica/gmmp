from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from reports.views import ReportView

urlpatterns = patterns('',
    url(r'^$', ReportView.as_view(), name='get_xlsx_reports'),
)
