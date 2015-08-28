import openpyxl
import json
import os
import logging

from reports.report_details import WS_INFO


RECODES = {
    'Caribbean': 'Carribean',
    'Pacific': 'Pacific Islands',
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
            json.dump(self.all_data, f)

    def get(self, new_ws):
        sheet = WS_INFO['ws_' + new_ws]

        if 'historical' not in sheet:
            raise KeyError('New worksheet %s is not linked to an historical worksheet' % new_ws)

        old_ws = sheet['historical']

        if old_ws not in self.all_data:
            raise KeyError('Old worksheet %s does not have any historical data' % new_ws)

        return self.all_data[sheet['historical']]

    def import_from_file(self, fname):
        # TODO: regional? country? global?
        wb = openpyxl.load_workbook(fname, read_only=True, data_only=True)

        for old_sheet, new_sheet in self.historical_sheets():
            ws = wb[old_sheet]

            self.log.info("Importing sheet %s" % old_sheet)
            data = getattr(self, 'import_%s' % old_sheet)(ws, new_sheet)
            self.log.info("Imported sheet %s" % old_sheet)

            self.all_data[old_sheet] = data

    def historical_sheets(self):
        return [(sheet['historical'], sheet) for sheet in WS_INFO.itervalues() if 'historical' in sheet]

    def import_1F(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}
        row_heading_col = 5

        for icol in xrange(15, 19):
            col_heading = canon(ws.cell(column=icol, row=4).value)
            col_data = {}
            data[col_heading] = col_data

            for irow in xrange(5, 12):
                row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                # TODO: normalise this?
                col_data[row_heading] = ws.cell(column=icol, row=irow).value

        return all_data
