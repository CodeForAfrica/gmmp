from .canon import canon
from ._base_importer import BaseReportImporter


class GMMP2015ReportImporter(BaseReportImporter):
    """
    Holds the methods that handles importing the GMMP 2015 final report
    """

    def __init__(self):
        BaseReportImporter.__init__(self)

    def slurp_table(
        self,
        ws,
        data,
        col_start,
        col_end,
        row_end,
        row_start=7,
        col_heading_row=5,
        row_heading_col=2,
    ):
        return super(GMMP2015ReportImporter, self).slurp_table(
            ws,
            data,
            col_start,
            col_end,
            row_end,
            row_start,
            col_heading_row,
            row_heading_col,
        )

    def import_1(self, sheet_info):
        all_data = {}
        for year, col_start, col_end, row_end in [
            (2015, 3, 10, 14),
            (2010, 13, 16, 14),
        ]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws, data, col_start=col_start, col_end=col_end, row_end=row_end
            )

        return all_data

    def import_5(self, sheet_info):
        data_for_2015 = {}
        all_data = {}
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
