from .canon import canon
from ._base_importer import BaseReportImporter


class GMMP2015ReportImporter(BaseReportImporter):
    """
    Holds the methods that handles importing the GMMP 2015 final report
    """

    def __init__(self):
        BaseReportImporter.__init__(self)
        self.year = 2015

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

    def import_grid(self, grid_info, all_data=None):
        all_data = {} if not all_data else all_data
        for year, col_start, col_end, row_start, row_end in grid_info:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_start=row_start,
                row_end=row_end
            )
        return all_data

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

    def import_2(self, sheet_info):
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 10),
            (2010, 13, 16)
        ]:
            data = {}
            all_data[year] = data
            regions = {
                'Africa': (7, 38),
                'Asia': (41, 51),
                'Caribbean': (54, 68),
                'Europe': (71, 100),
                'Latin America': (103, 116),
                'Middle East': (119, 124),
                'North America': (127, 128),
                'Pacific Island': (131, 134),
            }
            for region, (row_start, row_end) in regions.items():
                regional_data = dict()
                data[region] = regional_data

                self.slurp_table(
                    self.ws,
                    regional_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_3(self, sheet_info):
        all_data = {}
        for year, col_start, col_end, row_end in [
            (2015, 3, 7, 14),
            (2010, 10, 12, 14),
        ]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_end=row_end
            )

        return all_data

    def import_5(self, sheet_info):
        data_for_2015 = {}
        all_data = {}
        all_data[self.year] = data_for_2015
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

    def import_7(self, sheet_info):
        all_data = {}
        for year, col_start, col_end, row_end in [
            (2015, 3, 5, 8),
            (2010, 16, 19, 8),
            (2005, 13, 15, 8),
        ]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_end=row_end
            )

        return all_data

    def import_8(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 10),
                (2010, 9, 10, 7, 10),
                (2005, 8, 8, 7, 10),
                (2000, 7, 7, 7, 10),
                (1995, 6, 6, 7, 10),
            ]
        )

    def import_9(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 61),
                (2010, 6, 6, 7, 61),
            ]
        )

    def import_10(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 7, 7, 13),
            ]
        )

    def import_11(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 5, 7, 13),
            ]
        )

    def import_14(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 34),
                (2010, 9, 10, 7, 34),
                (2005, 8, 8, 7, 34),
                (2000, 7, 7, 7, 34),
                (1995, 6, 6, 7, 34),
            ]
        )

    def import_15(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 14),
                (2010, 9, 10, 7, 14),
                (2005, 8, 8, 7, 14),
                (2000, 7, 7, 7, 14),
                (1995, 6, 6, 7, 14),
            ]
        )

    def import_18(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 5, 7, 13),
                (2010, 7, 8, 7, 13),
                (2005, 9, 11, 7, 13),
            ]
        )

    def import_21(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=2,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=16,
            row_heading_col=2,
        )

        self.import_grid(
            [
                (1995, 9, 10, 7, 16),
                (2000, 11, 12, 7, 16),
                (2005, 13, 14, 7, 16),
                (2010, 15, 17, 7, 16),
            ],
            all_data=all_data
        )

        return all_data

    def import_23(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=2,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=16,
            row_heading_col=2,
        )

        self.import_grid(
            [
                (2005, 9, 10, 7, 16),
                (2010, 11, 13, 7, 16),
            ],
            all_data=all_data
        )

        return all_data

    def import_24(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 8),
                (2010, 11, 12, 7, 8),
                (2005, 9, 10, 7, 8),
                (2000, 8, 8, 7, 8),
                (1995, 7, 7, 7, 8),
            ]
        )

    def import_25(self, sheet_info):
        all_data = {}

        for year, col_start, cols, cols_per_group in [
            (2015, 3, 2, 2),
            (2010, 8, 2, 3),
        ]:
            data = {}
            all_data[year] = data
            self.slurp_secondary_col_table(
                self.ws,
                data,
                col_start=col_start,
                cols=cols,
                cols_per_group=cols_per_group,
                major_col_heading_row=5,
                row_start=8,
                row_end=9,
                row_heading_col=2,
            )

        return all_data

    def import_26(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 8),
                (2010, 10, 11, 7, 8),
                (2005, 8, 9, 7, 8),
                (2000, 6, 7, 7, 8),
            ]
        )

    def import_27(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 9),
                (2010, 10, 12, 7, 9),
                (2005, 8, 9, 7, 9),
                (2000, 6, 7, 7, 9),
            ]
        )

    def import_31(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 61),
                (2010, 6, 6, 7, 61),
            ]
        )

    def import_34(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 5, 7, 10),
                (2010, 9, 9, 7, 10),
                (2005, 8, 8, 7, 10),
                (2000, 7, 7, 7, 10),
            ]
        )

    def import_36(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 8),
                (2010, 8, 10, 7, 8),
                (2005, 6, 7, 7, 8),
            ]
        )

    def import_38(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 5, 7, 13),
            ]
        )

    def import_39(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 61),
                (2010, 6, 7, 7, 61),
            ]
        )

    def import_40(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=8,
            cols_per_group=1,
            major_col_heading_row=5,
            row_start=8,
            row_end=62,
            row_heading_col=2,
        )

        data_2010 = {}
        all_data[2010] = data_2010
        self.slurp_table(
            self.ws,
            data_2010,
            col_start=12,
            col_end=20,
            row_start=8,
            row_end=62,
            row_heading_col=2,
            col_heading_row=6,
        )

        return all_data

    def import_41(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=2,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=61,
            row_heading_col=2,
        )

        data_2010 = {}
        all_data[2010] = data_2010
        self.slurp_table(
            self.ws,
            data_2010,
            col_start=8,
            col_end=9,
            row_start=7,
            row_end=61,
            row_heading_col=2,
        )

        return all_data

    def import_42(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=8,
            cols_per_group=3,
            major_col_heading_row=5,
            row_start=8,
            row_end=62,
            row_heading_col=2,
        )

        return all_data

    def import_43(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=2,
            cols_per_group=3,
            major_col_heading_row=5,
            row_start=8,
            row_end=62,
            row_heading_col=2,
        )

        return all_data

    def import_44(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=2,
            cols_per_group=3,
            major_col_heading_row=5,
            row_start=8,
            row_end=15,
            row_heading_col=2,
        )

        data_2010 = {}
        all_data[2010] = data_2010
        self.slurp_table(
            self.ws,
            data_2010,
            col_start=10,
            col_end=12,
            row_start=8,
            row_end=15,
            row_heading_col=2,
            col_heading_row=6,
        )

        return all_data

    def import_45(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 5, 7, 14),
                (2010, 6, 9, 7, 14),
            ]
        )

    def import_46(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=8,
            cols_per_group=5,
            major_col_heading_row=5,
            row_start=8,
            row_end=14,
            row_heading_col=2,
        )

        return all_data

    def import_47(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 7, 7, 13),
            ]
        )

    def import_49(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 10, 7, 14),
            ]
        )

    def import_50(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 10, 7, 120),
            ]
        )

    def import_51(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 10, 7, 120),
            ]
        )

    def import_52(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 10, 7, 120),
            ]
        )

    def import_53(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=8,
            row_end=121,
            row_heading_col=2,
        )

        return all_data

    def import_54(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=7,
            cols_per_group=5,
            major_col_heading_row=5,
            row_start=8,
            row_end=121,
            row_heading_col=2,
        )

        return all_data

    def import_55(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 31, 7, 120),
            ]
        )

    def import_56(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 11, 7, 120),
            ]
        )

    def import_59(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 6, 7, 10),
            ]
        )

    def import_67(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 10, 7, 120),
            ]
        )

    def import_73(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 9),
            ]
        )

    def import_84(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=29,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=15,
            row_heading_col=2,
        )

        return all_data

    def import_85(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=9,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=15,
            row_heading_col=2,
        )

        return all_data

    def import_s12(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 9, 7, 120),
            ]
        )

    def import_s26(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        mediums = {
            'internet': (3, 9),
            'twitter': (12, 18),
        }

        for medium, (col_start, col_end) in mediums.items():
            medium_data = {}
            data[medium] = medium_data
            self.slurp_table(
                self.ws,
                medium_data,
                col_start=col_start,
                col_end=col_end,
                row_start=8,
                row_end=121,
                col_heading_row=6
            )

        return all_data

    def import_s27(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        mediums = {
            'internet': (3, 6),
            'twitter': (9, 12),
        }

        for medium, (col_start, col_end) in mediums.items():
            medium_data = {}
            data[medium] = medium_data
            self.slurp_table(
                self.ws,
                medium_data,
                col_start=col_start,
                col_end=col_end,
                row_start=8,
                row_end=121,
                col_heading_row=6
            )

        return all_data

    def import_sr08(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 9, 7, 15),
            ]
        )

    def import_s14(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=120,
            row_heading_col=2,
        )

        return all_data

    def import_s15(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=120,
            row_heading_col=2,
        )

        return all_data

    def import_s16(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=120,
            row_heading_col=2,
        )

        return all_data

    def import_s18(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        mediums = {
            'internet': (3, 2),
            'twitter': (10, 9),
        }

        for medium, (col_start, row_heading_col) in mediums.items():
            medium_data = {}
            data[medium] = medium_data

            self.slurp_secondary_col_table(
                self.ws,
                medium_data,
                col_start=col_start,
                cols=7,
                cols_per_group=2,
                major_col_heading_row=6,
                row_start=8,
                row_end=121,
                row_heading_col=row_heading_col,
            )

        return all_data

    def import_sr09(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=15,
            row_heading_col=2,
        )

        return all_data

    def import_sr10(self, sheet_info):
        data = {}
        all_data = {self.year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=3,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=5,
            row_start=7,
            row_end=15,
            row_heading_col=2,
        )

        return all_data
