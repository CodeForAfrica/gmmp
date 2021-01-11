from .base import BaseImport

from reports.utils.canon import canon
from .import_2010 import Import2010


class Import2015(BaseImport):
    """
        Holds the methods that handles importing 2015 data files
    """
    def __init__(self):
        self.ws = None
        self.old_sheet = None
        self.new_sheet = None
        self.import_2010 = Import2010()

    def get_work_sheet(self, wb, old_sheet, new_sheet):
        for name in wb.sheetnames:
            if name == new_sheet.get('name') or name.startswith(old_sheet + ' '):
                self.ws = wb[name]
                break
        self.import_2010.ws = self.ws
        return self.ws

    def import_sheet(self, old_sheet, new_sheet, all_data=None):
        self.old_sheet, self.new_sheet = old_sheet, new_sheet
        return getattr(self, 'import_%s' % new_sheet.get('name'))(new_sheet, all_data=all_data)

    def import_1(self, sheet_info, all_data=None):
        # setup dict for data
        data = {}
        all_data = dict() if not all_data else all_data
        all_data[2015] = data

        # import current year's data
        self.slurp_table(self.ws, data, col_start=3, col_end=10, row_end=14)

        # import previous year's data too
        self.import_2010.import_sheet(
            self.old_sheet,
            self.new_sheet,
            all_data=all_data,
            col_start=13,
            col_end=16,
        )
        return all_data

    def import_5(self, sheet_info, all_data=None):
        # setup dict for data
        data_for_2015 = {}
        all_data = dict() if not all_data else all_data
        all_data[2015] = data_for_2015

        # data needed to retrieve data from correct cells in work sheet
        col_start, col_end, row_end, row_start, col_heading_row, row_heading_col, publication_row = 3, 5, 14, 8, 6, 2, 5

        # import current year's data
        for publications in [3, 7]:
            publication_group = canon(self.ws.cell(column=publications, row=publication_row).value)
            data = {}
            data_for_2015[publication_group] = data

            self.slurp_table(self.ws, data, col_start, col_end, row_end, row_start, col_heading_row, row_heading_col)
            col_start, col_end = 7, 9

        # import previous year's data too
        self.import_2010.import_sheet(
            self.old_sheet,
            self.new_sheet,
            all_data=all_data,
            col_heading_row=6,
            row_start=8,
            row_end=14,
            col_start=12,
            row_heading_col=11,
        )

        return all_data
