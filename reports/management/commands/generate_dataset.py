import os
import csv
from django.core.management.base import BaseCommand

from reports.report_builder import XLSXReportBuilder
from reports.report_dataset import generate_chart_desc

from reports.forms import GlobalForm


class Command(BaseCommand):
    help = "Generates dataset from the GMMP report"

    def add_arguments(self, parser):
        parser.add_argument("-w","--worksheets", nargs="+", help="Worksheets to generate dataset", required=False)
        parser.add_argument("-d", "--dataset-details", action="store_true", help="Filename to store the selected worksheet details")

    def handle(self, *args, **options):
        # Create the dataset directory if it doesn't exist
        os.makedirs("dataset", exist_ok=True)
        if options['worksheets']:
            dataset_sheets = options['worksheets']
        else:
            dataset_sheets = ["ws_05", "ws_06", "ws_09", "ws_15",
                                "ws_28b", "ws_28c", "ws_30", "ws_38", "ws_41", "ws_47", "ws_48", 
                                "ws_83", "ws_85", "ws_92", "ws_93", "ws_97", "ws_100", "ws_101", 
                                "ws_102", "ws_104"]

        chart_filename = options.get("dataset-details") if options.get("dataset-details") else "gmmp_dataset"
        fieldnames = ['Title', 'Description']
        generate_chart_desc(chart_filename, dataset_sheets)

        form = GlobalForm()
        xlsx = XLSXReportBuilder(form).build(dataset_sheets=dataset_sheets)
