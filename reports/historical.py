import openpyxl
import json
import os
import logging
import re

from reports.report_details import WS_INFO
from reports.utils.canon import canon
from reports.imports.base import BaseImport
from reports.imports.import_2010 import Import2010
from reports.imports.import_2015 import Import2015


class Historical(BaseImport):
    log = logging.getLogger(__name__)

    def __init__(self, historical_file='historical.json'):
        self.fname = historical_file
        self.load()

    def load(self):
        if os.path.exists(self.fname):
            with open(self.fname, 'r') as f:
                self.all_data = json.load(f)
        else:
            self.all_data = {}

    def save(self):
        with open(self.fname, 'w') as f:
            json.dump(self.all_data, f, indent=2, sort_keys=True)

    def get(self, new_ws, coverage, region=None, country=None):
        if coverage == 'region':
            key = canon(region)
        elif coverage == 'country':
            key = canon(country)
        elif coverage == 'global':
            key = 'global'
        else:
            raise ValueError("Unknown coverage %s" % coverage)

        sheet = WS_INFO['ws_' + new_ws]

        if 'historical' not in sheet:
            raise KeyError('New worksheet %s is not linked to an historical worksheet' % new_ws)
        old_ws = sheet['historical']

        if old_ws not in self.all_data[key]:
            raise KeyError('Old worksheet %s does not have any historical data' % old_ws)

        return self.all_data[key][sheet['historical']]

    def import_from_file(self, fname, coverage, region=None, country=None, year=None):
        wb = openpyxl.load_workbook(fname, read_only=True, data_only=True)

        key = coverage
        if region:
            self.log.info("Importing for region %s" % region)
            key = canon(region)
        elif country:
            self.log.info("Importing for country %s" % country)
            key = canon(country)
        import_classes = {  # instantiate the classes we need for our imports
            "2010": Import2010(),
            "2015": Import2015(),
        }
        for old_sheet, new_sheet in self.historical_sheets(coverage):
            # find matching sheet name
            import_class = import_classes[year]
            ws = import_class.get_work_sheet(wb, old_sheet, new_sheet, year)
            if not ws:
                self.log.warn("Couldn't find historical sheet %s; only have these sheets available: %s" % (old_sheet,
                            ', '.join(sorted(wb.sheetnames))))
                continue

            self.log.info("Importing sheet %s" % old_sheet)
            data = import_class.import_data(ws, old_sheet, new_sheet)
            self.all_data.setdefault(key, {})[old_sheet][year] = data
            self.log.info("Imported sheet %s" % old_sheet)

    def historical_sheets(self, coverage):
        return [(sheet['historical'], sheet) for sheet in WS_INFO.values()
                if 'historical' in sheet and coverage in sheet['reports']]
