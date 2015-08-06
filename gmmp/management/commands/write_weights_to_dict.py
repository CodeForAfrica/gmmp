import csv
from pprint import pprint

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(args[0]) as csvfile:
            reader = csv.DictReader(csvfile)
            weights = []
            for row in reader:
                row['Twitter'] = 1
                weights.append(row)
            pprint(weights)
