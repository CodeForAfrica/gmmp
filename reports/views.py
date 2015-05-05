from django.views.generic import View
from django.shortcuts import render

from reports.forms import ReportFilterForm

class ReportView(View):
    template_name = 'growers/dashboard.html'

    def get(self, request, *args, **kwargs):
        report_filter = ReportFilterForm()
        context = {form = report_filter}
        return render(
            request,
            self.template_name,
            context)

    def post(self, request, *args, **kwargs):
        context = {form = report_filter}
        return render(
            request,
            self.template_name,
            context)
