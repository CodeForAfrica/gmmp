from django.views.generic import View
from django.shortcuts import render

from reports.forms import ReportFilterForm

class ReportView(View):
    template_name = 'report_filter.html'

    def get(self, request, *args, **kwargs):
        filter_form = ReportFilterForm()
        import ipdb; ipdb.set_trace()
        context = {'form' : filter_form}
        return render(
            request,
            self.template_name,
            context)

    def post(self, request, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        filter_form = ReportFilterForm(request.POST)
        if filter_form.is_valid():

        report_filter = ReportFilterForm()
        context = {'form' : filter_form}
        return render(
            request,
            self.template_name,
            context)
