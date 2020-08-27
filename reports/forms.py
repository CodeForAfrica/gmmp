from django import forms
from reports.report_details import get_countries, get_regions


class GlobalForm(forms.Form):
    pass

class CountryForm(forms.Form):
    # Only show countries for which data has been submitted

    country = forms.ChoiceField(
        label='Country',
        choices=get_countries)

    def get_form_countries(self):
        return get_countries()

    def filter_countries(self):
        if self.cleaned_data['country'] == 'ALL':
            return get_countries()
        else:
            return [(code, country) for code, country in get_countries() if code == self.cleaned_data['country']]

class RegionForm(forms.Form):

    region = forms.ChoiceField(
        label='Region',
        choices=get_regions)

    def get_form_regions(self):
        return get_regions()

