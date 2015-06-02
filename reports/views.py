# Python
from datetime import date

# Django
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

# 3rd Party
import xlsxwriter
from django_countries import countries

# Project
from reports.report_builder import XLSXReportBuilder, XLSXDataExportBuilder, get_active_countries


class ReportFilterForm(forms.Form):
    # Only show countries for which data has been submitted
    COUNTRIES = [('ALL', 'Global')] + get_active_countries()

    country = forms.ChoiceField(
        label='Country',
        choices=COUNTRIES)

    def get_countries(self):
        if self.cleaned_data['country'] == 'ALL':
            return [code for code, name in list(countries)]
        else:
            return [self.cleaned_data['country']]


class ReportView(View):
    template_name = 'report_filter.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportView, self).dispatch(*args, **kwargs)

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
            xlsx = XLSXReportBuilder(filter_form).build()

            choice = [country for code, country in filter_form.COUNTRIES if code == request.POST['country']][0]
            filename = 'GMMP Report: %s - %s' % (choice, date.today())

            response = HttpResponse(xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename
            return response
            # context = {'form' : filter_form}
            # return render(
            #     request,
            #     self.template_name,
            #     context)

        report_filter = ReportFilterForm()
        context = {'form' : filter_form}
        return render(
            request,
            self.template_name,
            context)


@user_passes_test(lambda u: u.is_superuser)
def data_export(request):
    if request.method == 'POST':
        xlsx = XLSXDataExportBuilder(request).build()
        filename = 'GMMP Data export'

        response = HttpResponse(xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename

        return response

    context = {}
    return render(
        request,
        'data_export.html',
        context)
