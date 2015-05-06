# Django
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse

# 3rd Party
import xlsxwriter

# Project
from reports.forms import ReportFilterForm
from reports.report_builder import XLSXReportBuilder

class ReportView(View):
    template_name = 'report_filter.html'

    def get(self, request, *args, **kwargs):
        filter_form = ReportFilterForm()
        context = {'form' : filter_form}
        return render(
            request,
            self.template_name,
            context)

    def post(self, request, *args, **kwargs):
        filter_form = ReportFilterForm(request.POST)
        if filter_form.is_valid():
            # country = filter_form.cleaned_data['country']
            # wb = xlsxwriter.Workbook('GMMP Report - %s.xlsx' % country)
            # ws = wb.add_worksheet('Countries per medium')
            xlsx = XLSXReportBuilder(filter_form).build()

            # Where should filename should be determined?

            filename = 'Report'
            response = HttpResponse(xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename
            return response

        report_filter = ReportFilterForm()
        context = {'form' : filter_form}
        return render(
            request,
            self.template_name,
            context)
