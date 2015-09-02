from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from reports.historical import Historical
from reports.report_details import REGION_COUNTRY_MAP


class Command(BaseCommand):
    help = 'Import historical GMMP data from an XLSX file'
    option_list = BaseCommand.option_list + (
        make_option('--global',
            action='store_true',
            help='Coverage is global'),
        make_option('--region REGION',
            action='store',
            dest='region',
            help='Import regional data for a region. One of: %s' % ', '.join(sorted(REGION_COUNTRY_MAP.keys())))
    )

    def handle(self, *args, **options):
        historical = Historical()
        coverage = None
        region = None

        if options['global']:
            coverage = 'global'
        elif options['region']:
            coverage = 'region'
            region = options['region']
        else:
            raise CommandError("Must specify --global or --region")

        for fname in args:
            historical.import_from_file(fname, coverage, region=region)

        historical.save()
