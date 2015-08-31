import openpyxl
import json
import os
import logging

from reports.report_details import WS_INFO


RECODES = {
    'Pacific': 'Pacific Islands',
    'Congo, Rep (Brazzaville)': 'Congo',
    'Congo, Dem Rep': 'Congo (the Democratic Republic of the)',
    'Bosnia & Herzegovina': 'Bosnia and Herzegovina',
    'St Lucia': 'Saint Lucia',
    'St. Vincent and The Grenadines': 'Saint Vincent and the Grenadines',
    'Trinidad & Tobago': 'Trinidad and Tobago',
}


def canon(key):
    return recode(key.strip()).lower()


def recode(v):
    return RECODES.get(v, v)


class Historical(object):
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

    def get(self, new_ws, coverage):
        sheet = WS_INFO['ws_' + new_ws]

        if 'historical' not in sheet:
            raise KeyError('New worksheet %s is not linked to an historical worksheet' % new_ws)
        old_ws = sheet['historical']

        if old_ws not in self.all_data[coverage]:
            raise KeyError('Old worksheet %s does not have any historical data' % old_ws)

        return self.all_data[coverage][sheet['historical']]

    def import_from_file(self, fname, coverage):
        # TODO: regional? country? global?
        wb = openpyxl.load_workbook(fname, read_only=True, data_only=True)

        for old_sheet, new_sheet in self.historical_sheets():
            ws = wb[old_sheet]

            self.log.info("Importing sheet %s" % old_sheet)
            data = getattr(self, 'import_%s' % old_sheet)(ws, new_sheet)
            self.log.info("Imported sheet %s" % old_sheet)

            if coverage not in self.all_data:
                self.all_data[coverage] = {}

            self.all_data[coverage][old_sheet] = data

    def historical_sheets(self):
        return [(sheet['historical'], sheet) for sheet in WS_INFO.itervalues() if 'historical' in sheet]

    def import_1F(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(ws, data, col_start=15, col_end=18, row_end=12)

        return all_data

    def import_2F(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(ws, data, col_start=15, col_end=18, row_start=6, row_end=114)

        return all_data

    def import_3aF(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(ws, data, col_start=6, col_end=13, row_end=11, col_heading_row=3)

        return all_data

    def import_9aF(self, ws, sheet_info):
        all_data = {}
        col_heading = canon('Female')

        for icol in xrange(7, 11):
            year = ws.cell(column=icol, row=4).value
            if year == 'N-F':
                year = 2010
                col_heading = canon('N')
            else:
                year = int(year)

            if year not in all_data:
                all_data[year] = {}

            data = all_data[year]
            col_data = {}
            data[col_heading] = col_data

            for irow in xrange(5, 13):
                row_heading = canon(ws.cell(column=5, row=irow).value)
                col_data[row_heading] = ws.cell(column=icol, row=irow).value

        return all_data

    def import_9bF(self, ws, sheet_info):
        all_data = {}
        for col_heading, col_start in [('Print', 8), ('Radio', 13), ('Television', 18)]:
            col_heading = canon(col_heading)

            for icol in xrange(col_start, col_start + 2):
                year = int(ws.cell(column=icol, row=3).value)

                if year not in all_data:
                    all_data[year] = {}

                data = all_data[year]
                col_data = {}
                data[col_heading] = col_data

                for irow in xrange(4, 6):
                    row_heading = canon(ws.cell(column=5, row=irow).value)
                    col_data[row_heading] = ws.cell(column=icol, row=irow).value
                    if year == 2010:
                        col_data[row_heading] = [col_data[row_heading], int(ws.cell(column=icol+1, row=irow).value)]

        return all_data

    def slurp_table(self, ws, data, col_start, col_end, row_end, row_start=5, col_heading_row=4, row_heading_col=5):
        for icol in xrange(col_start, col_end + 1):
            col_heading = canon(ws.cell(column=icol, row=col_heading_row).value)
            col_data = {}
            data[col_heading] = col_data

            for irow in xrange(row_start, row_end):
                row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                col_data[row_heading] = ws.cell(column=icol, row=irow).value
