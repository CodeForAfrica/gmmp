from .base import BaseImport

from reports.utils.canon import canon
from reports.utils.work_sheet_mapper import mapper as work_sheet_mapper

class Import2015(BaseImport):
    """
        Holds the methods that handles importing 2015 data files
    """
    def get_work_sheet(self, wb, old_sheet, year):
        ws = None
        for name in wb.sheetnames:
            if name == work_sheet_mapper[old_sheet] or name.startswith(old_sheet + ' '):
                ws = wb[name]
                break
        return ws

    def generate_data(self, ws, old_sheet, new_sheet):
        return getattr(self, 'import_%s' % work_sheet_mapper[old_sheet])(ws, new_sheet)

    def import_1(self, ws, sheet_info):
        data = {}
        self.slurp_table(ws, data, col_start=3, col_end=10, row_end=14)

        return data

    def import_5(self, ws, sheet_info):
        all_data = {}
        col_start, col_end, row_end, row_start, col_heading_row, row_heading_col, publication_row = 3, 5, 14, 8, 6, 2, 5

        for publications in [3, 7]:
            publication_group = canon(ws.cell(column=publications, row=publication_row).value)
            data = {}
            all_data[publication_group] = data

            self.slurp_table(ws, data, col_start, col_end, row_end, row_start, col_heading_row, row_heading_col)
            col_start, col_end = 7, 9

        return all_data
