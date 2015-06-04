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
from reports.report_builder import (
    XLSXReportBuilder, XLSXDataExportBuilder,
    get_countries, get_regions)


class GlobalForm(forms.Form):
    pass

class CountryForm(forms.Form):
    # Only show countries for which data has been submitted
    COUNTRIES = [('ALL', 'Global')] + get_countries()

    country = forms.ChoiceField(
        label='Country',
        choices=COUNTRIES)

    def filter_countries(self):
        if self.cleaned_data['country'] == 'ALL':
            return get_countries()
        else:
            return [self.cleaned_data['country']]

class RegionForm(forms.Form):
    REGIONS = [('ALL', 'Global')] + get_regions()

    region = forms.ChoiceField(
        label='Region',
        choices=REGIONS)


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
            choice = [country for code, country in form.COUNTRIES if code == request.POST['country']][0]
        elif 'region_form' in request.POST:
            form = RegionForm(request.POST)
            choice = [region for id, region in form.REGIONS if id == int(request.POST['region'])][0]
        else:
            form = GlobalForm(request.POST)
            choice = 'Global'

        if form.is_valid():
            xlsx = XLSXReportBuilder(form).build()
            filename = 'GMMP Report: %s - %s' % (choice, date.today())

            response = HttpResponse(xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename
            return response
            # context = {'form' : filter_form}
            # return render(
            #     request,
            #     self.template_name,
            #     context)

        report_filter = CountryForm()
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
