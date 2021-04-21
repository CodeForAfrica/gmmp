from django.urls import path
from django.views.generic.base import TemplateView
from reports.views import ReportView, WazimapView, data_export

urlpatterns = [
    path('', ReportView.as_view(), name='get_xlsx_reports'),
    path('data_export/', data_export, name='get_data_export'),
    path('wazimap', WazimapView.as_view(), name='wazimap'),
]
