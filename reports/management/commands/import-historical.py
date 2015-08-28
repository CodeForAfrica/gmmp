from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from reports.historical import Historical


class Command(BaseCommand):
    help = 'Import historical GMMP data from an XLSX file'
    option_list = BaseCommand.option_list + (
        make_option('--global',
            action='store_true',
            help='Coverage is global'),
        )

    def handle(self, *args, **options):
        historical = Historical()
        coverage = None

        if options['global']:
            coverage = 'global'
        else:
            raise CommandError("Must specify --global")

        for fname in args:
            historical.import_from_file(fname, coverage)

        historical.save()
