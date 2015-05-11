from django.core.management.base import BaseCommand
from forms.models import CountryRegion, sheet_models

class Command(BaseCommand):
    """
    This should be ported to a migration
    """
    help = 'Assign regions to Sheets'

    def handle(self, **options):
        for name, model in sheet_models.iteritems():
            sheets = model.objects.all()
            for sheet in sheets:
                try:
                    country_region = CountryRegion.objects.get(country=sheet.country.code)
                    sheet.country_region = country_region
                    sheet.save()
                except CountryRegion.DoesNotExist:
                    # Country is None
                    pass
