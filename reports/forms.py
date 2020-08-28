from django import forms
from reports.report_details import get_countries, get_regions


class GlobalForm(forms.Form):
    pass

class CountryForm(forms.Form):
    """
    Due to the system checks added in django 1.9 https://docs.djangoproject.com/en/3.1/releases/1.9/#urls,
    this form gets imported automatically when the url imports happen. This in turn causes the COUNTRIES = get_countries()
    variable to be called causing database query errors since migrations haven't been applied yet.
    Removing COUNTRIES = get_countries() and replacing it with get_form_countries ensures that the get_countries function
    will now only be explicitly called as opposed to being automatically called.
    """
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
    """
    Due to the system checks added in django 1.9 https://docs.djangoproject.com/en/3.1/releases/1.9/#urls,
    this form gets imported automatically when the url imports happen. This in turn causes the  REGIONS = get_regions()
    variable to be called causing database query errors since migrations haven't been applied yet.
    Removing REGIONS = get_regions() and replacing it with get_form_regions ensures that the get_regions function
    will now only be explicitly called as opposed to being automatically called.
    """

    region = forms.ChoiceField(
        label='Region',
        choices=get_regions)

    def get_form_regions(self):
        return get_regions()

