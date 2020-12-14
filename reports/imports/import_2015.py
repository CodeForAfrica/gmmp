from .base import BaseImport

from reports.utils.canon import canon

class Import2015(BaseImport):
    """
        Holds the methods that handles importing 2015 data files
    """
    def __init__(self):
        self.ws = None

    def get_work_sheet(self, wb, old_sheet, new_sheet):
        for name in wb.sheetnames:
            if name == new_sheet.get('name') or name.startswith(old_sheet + ' '):
                self.ws = wb[name]
                break
        return self.ws

    def import_sheet(self, old_sheet, new_sheet):
        return getattr(self, 'import_%s' % new_sheet.get('name'))(new_sheet)

    def import_1(self, sheet_info):
        data = {}
        self.slurp_table(self.ws, data, col_start=3, col_end=10, row_end=14)

        return data

    def import_5(self, sheet_info):
        all_data = {}
        col_start, col_end, row_end, row_start, col_heading_row, row_heading_col, publication_row = 3, 5, 14, 8, 6, 2, 5

        for publications in [3, 7]:
            publication_group = canon(self.ws.cell(column=publications, row=publication_row).value)
            data = {}
            all_data[publication_group] = data

            self.slurp_table(self.ws, data, col_start, col_end, row_end, row_start, col_heading_row, row_heading_col)
            col_start, col_end = 7, 9

        return all_data
