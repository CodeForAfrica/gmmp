from django.core.management.base import BaseCommand
from django.db.models import F
from forms.models import sheet_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        for name, model in sheet_models.items():
            country_errors_sheets = model.objects.exclude(monitor__country__in=F('country'))
            for sheet in country_errors_sheets:
                try:
                    sheet.country = sheet.monitor.country
                    sheet.save()
                    self.stdout.write("%s,%s" % (name, sheet.id))
                except AttributeError:
                    self.stdout.write("Sheet has no monitor: %s %s" % (name, sheet.id))

