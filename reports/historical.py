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
    'Female  %F': 'Female',
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
        self.slurp_year_grouped_table(ws, all_data, col_start=6, cols=1, cols_per_group=5, year_heading_row=4, col_heading_row=3, row_start=5, row_end=12)
        return all_data

    def import_9bF(self, ws, sheet_info):
        data = {}
        self.slurp_year_grouped_table(ws, data, col_start=6, cols=3, cols_per_group=5, year_heading_row=3, col_heading_row=2, row_start=4, row_end=5)
        return data

    def import_9cF(self, ws, sheet_info):
        data = {}
        self.slurp_year_grouped_table(ws, data, col_start=6, cols=1, cols_per_group=5, year_heading_row=3, col_heading_row=2, row_start=5, row_end=8)
        return data

    def slurp_table(self, ws, data, col_start, col_end, row_end, row_start=5, col_heading_row=4, row_heading_col=5):
        """
        Grab values from a simple table with column and row titles.
        """
        for icol in xrange(col_start, col_end + 1):
            col_heading = canon(ws.cell(column=icol, row=col_heading_row).value)
            col_data = {}
            data[col_heading] = col_data

            for irow in xrange(row_start, row_end):
                row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                col_data[row_heading] = ws.cell(column=icol, row=irow).value

    def slurp_year_grouped_table(self, ws, all_data, col_start, cols_per_group, cols, row_end, row_start=5, year_heading_row=4, col_heading_row=3, row_heading_col=5):
        """
        Slurp a table where each category contains a range of years.

        eg.
             Category 1      | Category 2      |
             2005 | 2010 | N | 2005 | 2010 | N |
        row1
        row2
        row3
        """
        for icol in xrange(col_start, col_start + cols * cols_per_group, cols_per_group):
            col_heading = canon(ws.cell(column=icol, row=col_heading_row).value)

            for iyear in xrange(icol, icol + cols_per_group):
                year = ws.cell(column=iyear, row=year_heading_row).value
                if year in ['N', 'N-F']:
                    year = 2010
                    effective_col_heading = canon('N')
                else:
                    year = int(year)
                    effective_col_heading = col_heading

                if year not in all_data:
                    all_data[year] = {}

                data = all_data[year]
                col_data = {}
                data[effective_col_heading] = col_data

                for irow in xrange(row_start, row_end + 1):
                    row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                    col_data[row_heading] = ws.cell(column=iyear, row=irow).value
