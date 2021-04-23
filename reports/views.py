# Python
from datetime import date

# Django
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

# Project
from reports.report_builder import XLSXReportBuilder

from reports.export_builder import XLSXDataExportBuilder
from reports.forms import GlobalForm, CountryForm, RegionForm


class ReportView(View):
    template_name = 'report_filter.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReportView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        country_form = CountryForm()
        region_form = RegionForm()
        context = {
            'country_form': country_form,
            'region_form': region_form}
        return render(
            request,
            self.template_name,
            context)

    def post(self, request, *args, **kwargs):
        if 'country_form' in request.POST:
            form = CountryForm(request.POST)
            choice = [country for code, country in form.get_form_countries() if code == request.POST['country']][0]
        elif 'region_form' in request.POST:
            form = RegionForm(request.POST)
            choice = [region for id, region in form.get_form_regions() if id == int(request.POST['region'])][0]
        else:
            form = GlobalForm(request.POST)
            choice = 'Global'

        if form.is_valid():
            xlsx = XLSXReportBuilder(form).build()
            filename = 'GMMP Report: %s - %s' % (choice, date.today())

            response = HttpResponse(xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
            return response
            # context = {'form' : filter_form}
            # return render(
            #     request,
            #     self.template_name,
            #     context)

        report_filter = CountryForm()
        context = {'form' : form}
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


class WazimapView(View):
    template_name = 'index.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name, {})
