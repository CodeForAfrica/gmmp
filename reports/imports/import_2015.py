from .base import BaseImport

from reports.utils.canon import canon

class Import2015(BaseImport):
    def import_1F(self, ws, sheet_info):
        data = {}
        self.slurp_table(ws, data, col_start=3, col_end=10, row_end=14)

        return data

    def import_9aF(self, ws, sheet_info):
        all_data = {}
        col_start, col_end, row_end, row_start, col_heading_row, row_heading_col, publication_row = 3, 5, 14, 8, 6, 2, 5

        for publications in [3, 7]:
            publication_group = canon(ws.cell(column=publications, row=publication_row).value)
            data = {}
            all_data[publication_group] = data

            self.slurp_table(ws, data, col_start, col_end, row_end, row_start, col_heading_row, row_heading_col)
            col_start, col_end = 7, 9

        return all_data
