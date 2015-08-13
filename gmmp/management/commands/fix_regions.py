import os
import csv
from collections import defaultdict
from django.core.management.base import BaseCommand
from forms.models import sheet_models
from forms.modelutils import CountryRegion

class Command(BaseCommand):

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        with open(file_path + "/bad_sheets.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            sheets_to_fix = defaultdict(list)
            for row in reader:
                sheets_to_fix[row['sheet_type']].append(row['id'])
        for sheet_type, sheet_ids in sheets_to_fix.iteritems():
            model = sheet_models[sheet_type]
            for obj_id in sheet_ids:
                sheet = model.objects.get(id=obj_id)
                sheet.country_region = CountryRegion.objects.get(country=sheet.country)
                sheet.save()
                self.stdout.write("%s %s" % (sheet_type, obj_id))
