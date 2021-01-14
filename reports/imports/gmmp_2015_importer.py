from reports.utils.canon import canon

from .base import BaseReportImporter


class GMMP2015ReportImporter(BaseReportImporter):
    """
    Holds the methods that handles importing 2015 data files
    """

    def __init__(self):
        self.ws = None

    def get_work_sheet(self, wb, sheet):
        for name in wb.sheetnames:
            if name == sheet.get("historical"):
                self.ws = wb[name]
                break
        return self.ws

    def import_sheet(self, sheet):
        return getattr(self, "import_%s" % sheet.get("historical"))(sheet)

    def import_1(self, sheet_info):
        data_for_2015 = {}
        data_for_2010 = {}
        all_data = dict()
        all_data[2015] = data_for_2015
        all_data[2010] = data_for_2010

        self.slurp_table(self.ws, data_for_2015, col_start=3, col_end=10, row_end=14)
        self.slurp_table(self.ws, data_for_2010, col_start=13, col_end=16, row_end=12)

        return all_data

    def import_5(self, sheet_info):
        data_for_2015 = {}
        all_data = dict()
        all_data[2015] = data_for_2015
        (
            col_start,
            col_end,
            row_end,
            row_start,
            col_heading_row,
            row_heading_col,
            publication_row,
        ) = (3, 5, 14, 8, 6, 2, 5)

        for publications in [3, 7]:
            publication_group = canon(
                self.ws.cell(column=publications, row=publication_row).value
            )
            data = {}
            data_for_2015[publication_group] = data

            self.slurp_table(
                self.ws,
                data,
                col_start,
                col_end,
                row_end,
                row_start,
                col_heading_row,
                row_heading_col,
            )
            col_start, col_end = 7, 9

        self.slurp_year_grouped_table(
            self.ws,
            all_data,
            col_start=12,
            cols=1,
            cols_per_group=5,
            year_heading_row=4,
            col_heading_row=6,
            row_start=8,
            row_end=14,
            row_heading_col=11,
        )

        return all_data
