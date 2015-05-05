from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from reports.views import ReportView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gmmp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', ReportView.as_view(template_name="get_xlsx_reports.html"), name='get_xlsx_reports'),
)
