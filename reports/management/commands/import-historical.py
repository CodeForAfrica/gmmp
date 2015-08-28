from django.core.management.base import BaseCommand
from reports.historical import Historical


class Command(BaseCommand):
    help = 'Import historical GMMP data from an XLSX file'

    def handle(self, *args, **options):
        historical = Historical()

        for fname in args:
            historical.import_from_file(fname)

        historical.save()
