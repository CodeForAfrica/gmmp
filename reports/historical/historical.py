import openpyxl
import json
import os
import logging
import re

from reports.report_details import WS_INFO

from .canon import canon
from ._gmmp_2010_importer import GMMP2010ReportImporter
from ._gmmp_2015_importer import GMMP2015ReportImporter


class Historical(object):
    log = logging.getLogger(__name__)

    def __init__(self, historical_file="historical.json"):
        self.fname = historical_file
        self.load()

    def load(self):
        if os.path.exists(self.fname):
            with open(self.fname, "r") as f:
                self.all_data = json.load(f)
        else:
            self.all_data = {}

    def save(self):
        with open(self.fname, "w") as f:
            json.dump(self.all_data, f, indent=2, sort_keys=True)

    def get(self, new_ws, coverage, region=None, country=None):
        if coverage == "region":
            key = canon(region)
        elif coverage == "country":
            key = canon(country)
        elif coverage == "global":
            key = "global"
        else:
            raise ValueError("Unknown coverage %s" % coverage)

        sheet = WS_INFO["ws_" + new_ws]

        if "historical" not in sheet:
            raise KeyError(
                "New worksheet %s is not linked to an historical worksheet" % new_ws
            )
        old_ws = sheet["historical"]

        if old_ws not in self.all_data[key]:
            raise KeyError(
                "Old worksheet %s does not have any historical data" % old_ws
            )

        return self.all_data[key][sheet["historical"]]

    def import_from_file(self, fname, coverage, region=None, country=None, year=None):
        wb = openpyxl.load_workbook(fname, read_only=True, data_only=True)

        key = coverage
        if region:
            self.log.info("Importing for region %s", region)
            key = canon(region)
        elif country:
            self.log.info("Importing for country %s", country)
            key = canon(country)
        report_importer_by_year = {
            "2010": GMMP2010ReportImporter,
            "2015": GMMP2015ReportImporter,
        }
        for sheet in self.historical_sheets(coverage, year):
            # find matching sheet name
            report_importer = report_importer_by_year[year]()
            ws = report_importer.get_work_sheet(wb, sheet)
            if not ws:
                self.log.warn(
                    "Couldn't find historical sheet %s; only have these sheets available: %s",
                    sheet.get("historical"),
                    ", ".join(sorted(wb.sheetnames)),
                )
                continue

            self.log.info(
                "Importing sheet %s of the %s report", sheet.get("historical"), year
            )
            data = report_importer.import_sheet(sheet)
            self.all_data.setdefault(key, {})[sheet.get("historical")] = data
            self.log.info(
                "Imported sheet %s of the %s report", sheet.get("historical"), year
            )

    def historical_sheets(self, coverage, year):
        sheets = []
        for sheets_by_year in WS_INFO.values():
            sheet = sheets_by_year.get(year)
            if sheet and ("historical" in sheet and coverage in sheet["reports"]):
                sheets.append(sheet)
        return sheets
