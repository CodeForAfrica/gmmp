import os
import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

from reports.report_builder import XLSXReportBuilder
from reports.report_details import WS_INFO

from reports.forms import GlobalForm


class Command(BaseCommand):
    help = "Generates dataset from the GMMP report"

    def add_arguments(self, parser):
        parser.add_argument("-w","--worksheets", nargs="+", help="Worksheets to generate dataset", required=False)
        parser.add_argument("-c", "--chart", action="store_true", help="Generate names and descriptions for Wazimap-NG chart.")
        parser.add_argument("-cf", "--chart-filename", action="store_true", help="Filename to store the Wazimap-NG chart descriptions")

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

        if options["chart"]:
            chart_filename = options.get("chart-filename") if options.get("chart-filename") else "gmmp_dataset"
            fieldnames = ['Title', 'Description']
            path = Path(f"/app/dataset/{chart_filename}.csv")
            with open(path, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for ws in WS_INFO:
                    if ws in dataset_sheets:
                        data = WS_INFO[ws][settings.REPORTS_HISTORICAL_YEAR]
                        title = data.get('title')
                        description = data.get('desc')
                        writer.writerow({'Title': title, 'Description': description})

        form = GlobalForm()
        xlsx = XLSXReportBuilder(form).build(dataset_sheets=dataset_sheets)
