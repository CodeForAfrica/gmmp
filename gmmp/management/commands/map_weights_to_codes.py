import csv
from pprint import pprint

from django.core.management.base import BaseCommand

from django_countries import countries
from forms.modelutils import CountryRegion

class Command(BaseCommand):
    args = 'input_file output_file'
    help = 'Maps the given country names to there codes and regions.'
    def handle(self, *args, **options):
        country_weightings = {}
        with open(args[1], 'wb') as output:
            with open(args[0]) as csvfile:
                writer = csv.writer(output)
                reader = csv.DictReader(csvfile)
                writer.writerow(['Country', 'Region', 'Print', 'Radio', 'TV', 'Online'])
                for row in reader:
                    if row['Country'] == "Ivory Coast":
                        row['Country'] = u"C\xf4te d'Ivoire"
                    code = countries.by_name(row['Country'])
                    region = CountryRegion.objects.get(country=code).region
                    if not code:
                        self.stdout.write('Country not found %s' % row['Country'])
                        break
                    writer.writerow([
                        code, region, row['Print'], row['Radio'], row['TV'], row['Online']
                        ])
                    country_weightings[code] = {
                        'Region': region,
                        'Print': row['Print'],
                        'Radio': row['Radio'],
                        'Television': row['TV'],
                        'Internet': row['Online']
                    }
                pprint(country_weightings)
