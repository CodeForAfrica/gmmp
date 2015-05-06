from django import forms
from django_countries import countries


class ReportFilterForm(forms.Form):
    COUNTRIES = ((code, name) for code, name in list(countries))

    country = forms.ChoiceField(
        label='Country',
        choices=COUNTRIES)
