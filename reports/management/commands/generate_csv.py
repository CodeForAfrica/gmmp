from django.core.management.base import BaseCommand
from reports.report_builder import XLSXReportBuilder

from reports.forms import GlobalForm,


class Command(BaseCommand):
    help = "Generates CSV's for the GMMP reports"

    def add_arguments(self, parser):
        parser.add_argument('-w','--worksheets', nargs='+', help='Worksheets to generate csv', required=False)

    def handle(self, *args, **options):
        if options['worksheets']:
            csv_sheets = options['worksheets']
        else:
            csv_sheets = ["ws_05", "ws_06", "ws_09", "ws_15",
                                "ws_28b", "ws_28c", "ws_30", "ws_38", "ws_41", "ws_47", "ws_48", 
                                "ws_83", "ws_85", "ws_92", "ws_93", "ws_97", "ws_100", "ws_101", 
                                "ws_102", "ws_104"]
        form = GlobalForm()
        xlsx = XLSXReportBuilder(form).build(csv_sheets=csv_sheets)
    