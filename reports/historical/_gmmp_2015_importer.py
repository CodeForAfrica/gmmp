from .canon import canon
from ._base_importer import BaseReportImporter
from reports.report_details import get_regions


class GMMP2015ReportImporter(BaseReportImporter):
    """
    Holds the methods that handles importing the GMMP 2015 final report
    """

    def __init__(self):
        BaseReportImporter.__init__(self)
        self.year = 2015
        # The continents in the sheet do not include 'pacific' but the get_regions()
        # function returns a list of which include 'pacific' so we're excluding that from
        # the list to be consistent with the sheet data
        self.REGIONS = [region.lower() for _, region in get_regions() if region.lower() != 'pacific']

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

    def import_4(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        col_start, end_index = 3, 50
        while col_start < end_index:
            for continent in self.REGIONS:
                continental_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    continental_data,
                    col_start=col_start,
                    cols=3,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=14,
                    row_heading_col=2,
                )
                data_2015[continent] = continental_data
                col_start += 6

        col_start, end_index = 53, 84
        while col_start < end_index:
            for continent in self.REGIONS:
                for medium in ['internet', 'twitter']:
                    medium_data = {}
                    self.slurp_secondary_col_table(
                        self.ws,
                        medium_data,
                        col_start=col_start,
                        cols=1,
                        cols_per_group=2,
                        major_col_heading_row=6,
                        row_start=8,
                        row_end=14,
                        row_heading_col=2,
                    )
                    data_2015[continent][medium] = medium_data[medium]
                    col_start += 2

        data_2010 = {}
        all_data[2010] = data_2010
        for col_start, col_end, row_start, row_end, col_heading_row in [
            (87, 94, 8, 14, 6),
        ]:
            self.slurp_table(
                self.ws,
                data_2010,
                col_start=col_start,
                col_end=col_end,
                row_start=row_start,
                row_end=row_end,
                col_heading_row=col_heading_row,
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

    def _sheet_6_secondary_import(self, data, medium, col_start, end_index):
        medium_data = {}
        medium_data[medium] = {}
        while col_start < end_index:
            for continent in self.REGIONS:
                continental_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    continental_data,
                    col_start=col_start,
                    cols=1,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=15,
                    row_heading_col=2,
                )
                medium_data[medium][continent] = continental_data
                col_start += 2
            data[medium] = medium_data[medium]

    def import_6(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_6_secondary_import(
            data=data_2015,
            medium='print, radio, television',
            col_start=3,
            end_index=18,
        )
        self._sheet_6_secondary_import(
            data=data_2015,
            medium='internet, twitter',
            col_start=21,
            end_index=36,
        )

        data_2010 = {}
        all_data[2010] = data_2010
        col_start, end_index = 39, 54
        while col_start < end_index:
            for continent in self.REGIONS:
                continental_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    continental_data,
                    col_start=col_start,
                    cols=1,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=15,
                    row_heading_col=2,
                )
                data_2010[continent] = continental_data
                col_start += 2

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

    def import_12(self, sheet_info):
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
            row_end=14,
            row_heading_col=2,
        )

        return all_data

    def import_13(self, sheet_info):
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
            row_end=14,
            row_heading_col=2,
        )

        return all_data

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

    def import_16(self, sheet_info):
        all_data = {}

        for year, col_start, cols, cols_per_group in [
            (2015, 3, 8, 2),
            (2010, 21, 7, 2),
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
                row_end=35,
                row_heading_col=2,
            )

        return all_data

    def import_17(self, sheet_info):
        all_data = {}

        for year, col_start, cols, cols_per_group in [
            (2015, 3, 7, 2),
            (2010, 19, 6, 2),
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
                row_end=15,
                row_heading_col=2,
            )

        return all_data

    def import_18(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 5, 7, 13),
                (2010, 7, 8, 7, 13),
                (2005, 9, 11, 7, 13),
            ]
        )

    def import_19(self, sheet_info):
        all_data = {}

        for year, col_start, cols, cols_per_group in [
            (2015, 3, 1, 3),
            (2005, 7, 1, 2),
            (2010, 9, 1, 3),
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
                row_end=14,
                row_heading_col=2,
            )

        return all_data

    def import_20(self, sheet_info):
        all_data = {}

        for year, col_start, cols, cols_per_group in [
            (2015, 3, 8, 2),
            (2010, 21, 7, 2),
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
                row_end=35,
                row_heading_col=2,
            )

        return all_data

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

    def import_28(self, sheet_info):
        data_2015 = {}
        all_data = {2015: data_2015}

        mediums = ['print', 'radio', 'television']

        col_start, end_index = 3, 14
        while col_start <= end_index:
            for medium in mediums:
                medium_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    medium_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=15,
                    row_heading_col=2,
                )
                data_2015[medium] = medium_data
                col_start += 4

        for year, col_start, col_end, row_start, row_end, col_heading_row in [
            (1995, 17, 17, 8, 15, 6),
            (2000, 18, 18, 8, 15, 6),
            (2005, 19, 19, 8, 15, 6),
            (2010, 20, 21, 8, 15, 6),
        ]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_start=row_start,
                row_end=row_end,
                col_heading_row=col_heading_row,
            )

        return all_data

    def import_29(self, sheet_info):
        data_2015 = {}
        all_data = {2015: data_2015}

        col_start, end_index = 3, 34
        while col_start < end_index:
            for continent in self.REGIONS:
                continental_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    continental_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=11,
                    row_heading_col=2,
                )
                data_2015[continent] = continental_data
                col_start += 4

        return all_data

    def import_30(self, sheet_info):
        data_2015 = {}
        all_data = {2015: data_2015}

        col_start, end_index = 3, 34
        while col_start < end_index:
            for continent in self.REGIONS:
                continental_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    continental_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=14,
                    row_heading_col=2,
                )
                data_2015[continent] = continental_data
                col_start += 4

        return all_data

    def import_31(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 61),
                (2010, 6, 6, 7, 61),
            ]
        )

    def import_32(self, sheet_info):
        data_2015 = {}
        all_data = {2015: data_2015}

        mediums = ['print', 'radio', 'television']

        col_start, end_index = 3, 14
        while col_start < end_index:
            for medium in mediums:
                medium_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    medium_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=62,
                    row_heading_col=2,
                )
                data_2015[medium] = medium_data
                col_start += 4

        return all_data

    def import_35(self, sheet_info):
        data_2015 = {}
        all_data = {2015: data_2015}

        mediums = [
            'Anchor, announcer or presenter: Usually in the television studio',
            'Reporter: Usually outside the studio. Include reporters who do not appear on screen, but whose voice is heard (e.g. as voice-over).',
        ]

        col_start, end_index = 3, 10
        while col_start < end_index:
            for medium in mediums:
                medium_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    medium_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=14,
                    row_heading_col=2,
                )
                data_2015[medium] = medium_data
                col_start += 4

        data_2005 = {}
        all_data[2005] = data_2005
        col_start, end_index = 12, 13
        while col_start < end_index:
            for medium in mediums:
                medium_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    medium_data,
                    col_start=col_start,
                    cols=1,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=14,
                    row_heading_col=2,
                )
                data_2005[medium] = medium_data
                col_start += 1

        data_2010 = {}
        all_data[2010] = data_2010
        col_start, end_index = 14, 17
        while col_start < end_index:
            for medium in mediums:
                medium_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    medium_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=14,
                    row_heading_col=2,
                )
                data_2010[medium] = medium_data
                col_start += 2

        return all_data

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

    def import_48(self, sheet_info):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 18
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=4,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=14,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 8

        return all_data

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

    def import_57(self, sheet_info):
        from .utils.countries.countries_for_57 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 7),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_58(self, sheet_info):
        from .utils.countries.countries_for_58 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 7),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_59(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 6, 7, 10),
            ]
        )

    def import_60(self, sheet_info):
        from .utils.countries.countries_for_60 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 7),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_61(self, sheet_info):
        from .utils.countries.countries_for_57 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 7),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_62(self, sheet_info):
        from .utils.countries.countries_for_57 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 58),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_63(self, sheet_info):
        from .utils.countries.countries_for_66 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 58),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_64(self, sheet_info):
        from .utils.countries.countries_for_57 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 58),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_65(self, sheet_info):
        from .utils.countries.countries_for_57 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 9),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_66(self, sheet_info):
        from .utils.countries.countries_for_66 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 10),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_67(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 10, 7, 120),
            ]
        )

    def import_68(self, sheet_info):
        from .utils.countries.countries_for_57 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 9),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_68b(self, sheet_info):
        from .utils.countries.countries_for_66 import COUNTRIES
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 10),
        ]:
            data = {}
            all_data[year] = data

            for country, (row_start, row_end) in COUNTRIES.items():
                country_data = {}
                data[country] = country_data

                self.slurp_table(
                    self.ws,
                    country_data,
                    col_start=col_start,
                    col_end=col_end,
                    row_start=row_start,
                    row_end=row_end,
                )
        return all_data

    def import_71(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = ['political participation', 'peace and security', 'economic participation']

        col_start, end_index = 3, 17
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=5,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 5

        return all_data

    def import_72(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = ['political participation', 'peace and security', 'economic participation']

        col_start, end_index = 3, 17
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=5,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 5

        return all_data

    def import_73(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 4, 7, 9),
            ]
        )

    def _sheet_74_secondary_import(self, data, groups, medium, col_start, end_index, cols_per_group, multiplier):
        # groups = ['political participation', 'peace and security', 'economic participation']
        medium_data = {}
        medium_data[medium] = {}
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=3,
                    cols_per_group=cols_per_group,
                    major_col_heading_row=6,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                medium_data[medium][group] = group_data[group]
                col_start += multiplier
            data[medium] = medium_data[medium]

    def import_74(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_74_secondary_import(
            data=data_2015,
            groups=['political participation', 'peace and security', 'economic participation'],
            medium='print, radio, television',
            col_start=3,
            end_index=11,
            cols_per_group=3,
            multiplier=3,
        )

        self._sheet_74_secondary_import(
            data=data_2015,
            medium='internet, twitter',
            groups=['political participation', 'peace and security', 'economic participation'],
            col_start=14,
            end_index=22,
            cols_per_group=3,
            multiplier=3
        )

        return all_data

    def import_75(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_74_secondary_import(
            data=data_2015,
            groups=['political participation', 'peace and security', 'economic participation'],
            medium='print, radio, television',
            col_start=3,
            end_index=17,
            cols_per_group=5,
            multiplier=5
        )

        self._sheet_74_secondary_import(
            data=data_2015,
            groups=['political participation', 'peace and security', 'economic participation'],
            medium='internet, twitter',
            col_start=20,
            end_index=34,
            cols_per_group=5,
            multiplier=5
        )

        return all_data

    def import_76(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_74_secondary_import(
            data=data_2015,
            groups=['political participation', 'peace and security', 'economic participation'],
            medium='print, radio, television',
            col_start=3,
            end_index=11,
            cols_per_group=3,
            multiplier=3
        )

        self._sheet_74_secondary_import(
            data=data_2015,
            groups=['political participation', 'peace and security', 'economic participation'],
            medium='internet, twitter',
            col_start=14,
            end_index=22,
            cols_per_group=3,
            multiplier=3
        )

        return all_data

    def import_77(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = ['political participation', 'peace and security', 'economic participation']

        first_data = {}
        data_2015['Print, Radio, Television'] = first_data
        col_start, end_index = 3, 35
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=11,
                    cols_per_group=1,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                first_data[group] = group_data
                col_start += 11

        second_data = {}
        data_2015['Internet, Twitter'] = second_data
        col_start, end_index = 38, 70
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=11,
                    cols_per_group=1,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                second_data[group] = group_data
                col_start += 11

        return all_data

    def import_78(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = ['political participation', 'peace and security', 'economic participation']

        first_data = {}
        data_2015['Print, Radio, Television'] = first_data
        col_start, end_index = 3, 35
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=11,
                    cols_per_group=1,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                first_data[group] = group_data
                col_start += 11

        second_data = {}
        data_2015['Internet, Twitter'] = second_data
        col_start, end_index = 38, 70
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=11,
                    cols_per_group=1,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                second_data[group] = group_data
                col_start += 11

        return all_data

    def import_79(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 37
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=5,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 5

        return all_data

    def _sheet_80_secondary_import(self, data, groups, medium, col_start, end_index, row_end=17):
        local_data = {}
        data[medium] = local_data
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=row_end,
                    row_heading_col=2,
                )
                local_data[group] = group_data
                col_start += 4

    def import_80(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Women politicians, women electoral candidates...',
                'Peace, negotiations, treaties',
                'Other domestic politics, government, etc.',
                'Global partnerships',
                'Foreign/international politics, UN, peacekeeping',
                'National defence, military spending, internal security, etc.',
                'Other stories on politics (specify in comments)',
            ],
            medium='Politics and Government',
            col_start=3,
            end_index=30,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Economic policies, strategies, modules, indicators, stock markets, etc',
                'Economic crisis, state bailouts of companies, company takeovers and mergers, etc.',
                'Poverty, housing, social welfare, aid, etc.',
                'Womens participation in economic processes',
                'Employment',
                'Informal work, street vending, etc.',
                'Other labour issues (strikes, trade unions, etc.)',
                'Rural economy, agriculture, farming, land rights',
                'Consumer issues, consumer protection, fraud...',
                'Transport, traffic, roads...',
                'Other stories on economy (specify in comments)'
            ],
            medium='Economy',
            col_start=31,
            end_index=74,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Science, technology, research, discoveries...',
                'Medicine, health, hygiene, safety, (not EBOLA or HIV/AIDS)',
                'EBOLA, treatment, response...',
                'HIV and AIDS, policy, treatment, etc',
                'Other epidemics, viruses, contagions, Influenza, BSE, SARS',
                'Birth control, fertility, sterilization, termination...',
                'Climate change, global warming',
                'Environment, pollution, tourism',
                'Other stories on science (specify in comments)',
            ],
            medium='Science and Health',
            col_start=75,
            end_index=110,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Millennium Development Goals (MDGs), Post 2015 agenda, Sustainable Development Goals',
                'Family relations, inter-generational conflict, parents',
                'Human rights, womens rights, rights of sexual minorities, rights of religious minorities, etc.',
                'Religion, culture, tradition, controversies...',
                'Migration, refugees, xenophobia, ethnic conflict...',
                'Other development issues, sustainability, etc.',
                'Education, childcare, nursery, university, literacy',
                'Womens movement, activism, demonstrations, etc',
                'Changing gender relations (outside the home)',
                'Family law, family codes, property law, inheritance...',
                'Legal system, judiciary, legislation apart from family',
                'Disaster, accident, famine, flood, plane crash, etc.',
                'Riots, demonstrations, public disorder, etc.',
                'Other stories on social/legal (specify in comments)'
            ],
            medium='Social and Legal',
            col_start=111,
            end_index=166,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Non-violent crime, bribery, theft, drugs, corruption',
                'Violent crime, murder, abduction, assault, etc.',
                'Gender violence based on culture, family, inter-personal relations, feminicide, harassment, rape, sexual assault, trafficking, FGM...',
                'Gender violence perpetuated by the State',
                'Child abuse, sexual violence against children, neglect',
                'War, civil war, terrorism, other state-based violence',
                'Other crime/violence (specify in comments)'
            ],
            medium='Crime and Violence',
            col_start=167,
            end_index=194,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Celebrity news, births, marriages, royalty, etc.',
                'Arts, entertainment, leisure, cinema, books, dance',
                'Media, (including internet), portrayal of women/men',
                'Beauty contests, models, fashion, cosmetic surgery',
                'Sports, events, players, facilities, training, funding',
                'Other celebrity/arts/media news (specify in comments)',
            ],
            medium='Celebrity, Arts and Media, Sports',
            col_start=195,
            end_index=218,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Other (only use as a last resort & explain)',
            ],
            medium='Other',
            col_start=219,
            end_index=222,
        )

        return all_data

    def import_81(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Women politicians, women electoral candidates...',
                'Peace, negotiations, treaties',
                'Other domestic politics, government, etc.',
                'Global partnerships',
                'Foreign/international politics, UN, peacekeeping',
                'National defence, military spending, internal security, etc.',
                'Other stories on politics (specify in comments)',
            ],
            medium='Politics and Government',
            col_start=3,
            end_index=30,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Economic policies, strategies, modules, indicators, stock markets, etc',
                'Economic crisis, state bailouts of companies, company takeovers and mergers, etc.',
                'Poverty, housing, social welfare, aid, etc.',
                'Womens participation in economic processes',
                'Employment',
                'Informal work, street vending, etc.',
                'Other labour issues (strikes, trade unions, etc.)',
                'Rural economy, agriculture, farming, land rights',
                'Consumer issues, consumer protection, fraud...',
                'Transport, traffic, roads...',
                'Other stories on economy (specify in comments)'
            ],
            medium='Economy',
            col_start=31,
            end_index=74,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Science, technology, research, discoveries...',
                'Medicine, health, hygiene, safety, (not EBOLA or HIV/AIDS)',
                'EBOLA, treatment, response...',
                'HIV and AIDS, policy, treatment, etc',
                'Other epidemics, viruses, contagions, Influenza, BSE, SARS',
                'Birth control, fertility, sterilization, termination...',
                'Climate change, global warming',
                'Environment, pollution, tourism',
                'Other stories on science (specify in comments)',
            ],
            medium='Science and Health',
            col_start=75,
            end_index=110,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Millennium Development Goals (MDGs), Post 2015 agenda, Sustainable Development Goals',
                'Family relations, inter-generational conflict, parents',
                'Human rights, womens rights, rights of sexual minorities, rights of religious minorities, etc.',
                'Religion, culture, tradition, controversies...',
                'Migration, refugees, xenophobia, ethnic conflict...',
                'Other development issues, sustainability, etc.',
                'Education, childcare, nursery, university, literacy',
                'Womens movement, activism, demonstrations, etc',
                'Changing gender relations (outside the home)',
                'Family law, family codes, property law, inheritance...',
                'Legal system, judiciary, legislation apart from family',
                'Disaster, accident, famine, flood, plane crash, etc.',
                'Riots, demonstrations, public disorder, etc.',
                'Other stories on social/legal (specify in comments)'
            ],
            medium='Social and Legal',
            col_start=111,
            end_index=166,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Non-violent crime, bribery, theft, drugs, corruption',
                'Violent crime, murder, abduction, assault, etc.',
                'Gender violence based on culture, family, inter-personal relations, feminicide, harassment, rape, sexual assault, trafficking, FGM...',
                'Gender violence perpetuated by the State',
                'Child abuse, sexual violence against children, neglect',
                'War, civil war, terrorism, other state-based violence',
                'Other crime/violence (specify in comments)'
            ],
            medium='Crime and Violence',
            col_start=167,
            end_index=194,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Celebrity news, births, marriages, royalty, etc.',
                'Arts, entertainment, leisure, cinema, books, dance',
                'Media, (including internet), portrayal of women/men',
                'Beauty contests, models, fashion, cosmetic surgery',
                'Sports, events, players, facilities, training, funding',
                'Other celebrity/arts/media news (specify in comments)',
            ],
            medium='Celebrity, Arts and Media, Sports',
            col_start=195,
            end_index=218,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Other (only use as a last resort & explain)',
            ],
            medium='Other',
            col_start=219,
            end_index=222,
        )

        return all_data

    def import_82(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Women politicians, women electoral candidates...',
                'Peace, negotiations, treaties',
                'Other domestic politics, government, etc.',
                'Global partnerships',
                'Foreign/international politics, UN, peacekeeping',
                'National defence, military spending, internal security, etc.',
                'Other stories on politics (specify in comments)',
            ],
            medium='Politics and Government',
            col_start=3,
            end_index=30,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Economic policies, strategies, modules, indicators, stock markets, etc',
                'Economic crisis, state bailouts of companies, company takeovers and mergers, etc.',
                'Poverty, housing, social welfare, aid, etc.',
                'Womens participation in economic processes',
                'Employment',
                'Informal work, street vending, etc.',
                'Other labour issues (strikes, trade unions, etc.)',
                'Rural economy, agriculture, farming, land rights',
                'Consumer issues, consumer protection, fraud...',
                'Transport, traffic, roads...',
                'Other stories on economy (specify in comments)'
            ],
            medium='Economy',
            col_start=31,
            end_index=74,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Science, technology, research, discoveries...',
                'Medicine, health, hygiene, safety, (not EBOLA or HIV/AIDS)',
                'EBOLA, treatment, response...',
                'HIV and AIDS, policy, treatment, etc',
                'Other epidemics, viruses, contagions, Influenza, BSE, SARS',
                'Birth control, fertility, sterilization, termination...',
                'Climate change, global warming',
                'Environment, pollution, tourism',
                'Other stories on science (specify in comments)',
            ],
            medium='Science and Health',
            col_start=75,
            end_index=110,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Millennium Development Goals (MDGs), Post 2015 agenda, Sustainable Development Goals',
                'Family relations, inter-generational conflict, parents',
                'Human rights, womens rights, rights of sexual minorities, rights of religious minorities, etc.',
                'Religion, culture, tradition, controversies...',
                'Migration, refugees, xenophobia, ethnic conflict...',
                'Other development issues, sustainability, etc.',
                'Education, childcare, nursery, university, literacy',
                'Womens movement, activism, demonstrations, etc',
                'Changing gender relations (outside the home)',
                'Family law, family codes, property law, inheritance...',
                'Legal system, judiciary, legislation apart from family',
                'Disaster, accident, famine, flood, plane crash, etc.',
                'Riots, demonstrations, public disorder, etc.',
                'Other stories on social/legal (specify in comments)'
            ],
            medium='Social and Legal',
            col_start=111,
            end_index=166,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Non-violent crime, bribery, theft, drugs, corruption',
                'Violent crime, murder, abduction, assault, etc.',
                'Gender violence based on culture, family, inter-personal relations, feminicide, harassment, rape, sexual assault, trafficking, FGM...',
                'Gender violence perpetuated by the State',
                'Child abuse, sexual violence against children, neglect',
                'War, civil war, terrorism, other state-based violence',
                'Other crime/violence (specify in comments)'
            ],
            medium='Crime and Violence',
            col_start=167,
            end_index=194,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Celebrity news, births, marriages, royalty, etc.',
                'Arts, entertainment, leisure, cinema, books, dance',
                'Media, (including internet), portrayal of women/men',
                'Beauty contests, models, fashion, cosmetic surgery',
                'Sports, events, players, facilities, training, funding',
                'Other celebrity/arts/media news (specify in comments)',
            ],
            medium='Celebrity, Arts and Media, Sports',
            col_start=195,
            end_index=218,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Other (only use as a last resort & explain)',
            ],
            medium='Other',
            col_start=219,
            end_index=222,
        )

        return all_data

    def import_83(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 37
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=5,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 5

        return all_data

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

    def import_86(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 10
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 2

        return all_data

    def import_87(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 14
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=3,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 6

        return all_data

    def import_88(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 10
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 4

        return all_data

    def import_89(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 30
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=7,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 14

        return all_data

    def import_90(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 10
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 4

        return all_data

    def import_91(self, sheet_info):
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 10),
        ]:
            data = {}
            all_data[year] = data
            regions = {
                'Africa': (7, 8),
                'Asia': (9, 10),
                'Caribbean': (11, 12),
                'Europe': (13, 14),
                'Latin America': (15, 16),
                'Middle East': (17, 18),
                'North America': (19, 20),
                'Pacific Island': (21, 22),
                'Transnational': (23, 24),
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

    def import_92(self, sheet_info):
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 10),
        ]:
            data = {}
            all_data[year] = data
            regions = {
                'Africa': (7, 10),
                'Asia': (11, 14),
                'Caribbean': (15, 18),
                'Europe': (19, 22),
                'Latin America': (23, 26),
                'Middle East': (27, 30),
                'North America': (31, 34),
                'Pacific Island': (35, 38),
                'Transnational': (39, 42),
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

    def import_93(self, sheet_info):
        all_data = {}
        for year, col_start, col_end in [
            (2015, 3, 10),
        ]:
            data = {}
            all_data[year] = data
            regions = {
                'Africa': (7, 8),
                'Asia': (9, 10),
                'Caribbean': (11, 12),
                'Europe': (13, 14),
                'Latin America': (15, 16),
                'Middle East': (17, 18),
                'North America': (19, 20),
                'Pacific Island': (21, 22),
                'Transnational': (23, 24),
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

    def import_94(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 23
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=3,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 3

        return all_data

    def import_95(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Women politicians, women electoral candidates...',
                'Peace, negotiations, treaties',
                'Other domestic politics, government, etc.',
                'Global partnerships',
                'Foreign/international politics, UN, peacekeeping',
                'National defence, military spending, internal security, etc.',
                'Other stories on politics (specify in comments)',
            ],
            medium='Politics and Government',
            col_start=3,
            end_index=30,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Economic policies, strategies, modules, indicators, stock markets, etc',
                'Economic crisis, state bailouts of companies, company takeovers and mergers, etc.',
                'Poverty, housing, social welfare, aid, etc.',
                'Womens participation in economic processes',
                'Employment',
                'Informal work, street vending, etc.',
                'Other labour issues (strikes, trade unions, etc.)',
                'Rural economy, agriculture, farming, land rights',
                'Consumer issues, consumer protection, fraud...',
                'Transport, traffic, roads...',
                'Other stories on economy (specify in comments)'
            ],
            medium='Economy',
            col_start=31,
            end_index=74,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Science, technology, research, discoveries...',
                'Medicine, health, hygiene, safety, (not EBOLA or HIV/AIDS)',
                'EBOLA, treatment, response...',
                'HIV and AIDS, policy, treatment, etc',
                'Other epidemics, viruses, contagions, Influenza, BSE, SARS',
                'Birth control, fertility, sterilization, termination...',
                'Climate change, global warming',
                'Environment, pollution, tourism',
                'Other stories on science (specify in comments)',
            ],
            medium='Science and Health',
            col_start=75,
            end_index=110,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Millennium Development Goals (MDGs), Post 2015 agenda, Sustainable Development Goals',
                'Family relations, inter-generational conflict, parents',
                'Human rights, womens rights, rights of sexual minorities, rights of religious minorities, etc.',
                'Religion, culture, tradition, controversies...',
                'Migration, refugees, xenophobia, ethnic conflict...',
                'Other development issues, sustainability, etc.',
                'Education, childcare, nursery, university, literacy',
                'Womens movement, activism, demonstrations, etc',
                'Changing gender relations (outside the home)',
                'Family law, family codes, property law, inheritance...',
                'Legal system, judiciary, legislation apart from family',
                'Disaster, accident, famine, flood, plane crash, etc.',
                'Riots, demonstrations, public disorder, etc.',
                'Other stories on social/legal (specify in comments)'
            ],
            medium='Social and Legal',
            col_start=111,
            end_index=166,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Non-violent crime, bribery, theft, drugs, corruption',
                'Violent crime, murder, abduction, assault, etc.',
                'Gender violence based on culture, family, inter-personal relations, feminicide, harassment, rape, sexual assault, trafficking, FGM...',
                'Gender violence perpetuated by the State',
                'Child abuse, sexual violence against children, neglect',
                'War, civil war, terrorism, other state-based violence',
                'Other crime/violence (specify in comments)'
            ],
            medium='Crime and Violence',
            col_start=167,
            end_index=194,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Celebrity news, births, marriages, royalty, etc.',
                'Arts, entertainment, leisure, cinema, books, dance',
                'Media, (including internet), portrayal of women/men',
                'Beauty contests, models, fashion, cosmetic surgery',
                'Sports, events, players, facilities, training, funding',
                'Other celebrity/arts/media news (specify in comments)',
            ],
            medium='Celebrity, Arts and Media, Sports',
            col_start=195,
            end_index=218,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Other (only use as a last resort & explain)',
            ],
            medium='Other',
            col_start=219,
            end_index=222,
        )

        return all_data

    def import_96(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 23
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=3,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 3

        return all_data

    def import_97(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 37
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=5,
                    cols_per_group=1,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 5

        return all_data

    def import_s01(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        categories = ['presenter', 'reporter', 'subjects']

        col_start, end_index = 3, 14
        while col_start < end_index:
            for category in categories:
                category_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    category_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[category] = category_data
                col_start += 4

        return all_data

    def import_s02(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        mediums = ['print', 'radio', 'television']

        col_start, end_index = 3, 14
        while col_start < end_index:
            for medium in mediums:
                medium_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    medium_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[medium] = medium_data
                col_start += 4

        return all_data

    def import_s03(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 30
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_s04(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'not stated', 'royalty, monarch, deposed monarch, etc.',
            'government, politician, minister, spokesperson...', 'government employee, public servant, etc.',
            'police, military, para-military, militia, fire officer', 'academic expert, lecturer, teacher',
            'doctor, dentist, health specialist', 'health worker, social worker, childcare worker',
            'science/technology professional, engineer, etc.', 'media professional, journalist, film-maker, etc.',
            'lawyer, judge, magistrate, legal advocate, etc.', 'business person, exec, manager, stock broker...',
            'office or service worker, non-management worker', 'tradesperson, artisan, labourer, truck driver, etc.',
            'agriculture, mining, fishing, forestry', 'religious figure, priest, monk, rabbi, mullah, nun',
            'activist or worker in civil society org., ngo, trade union', 'sex worker',
            'celebrity, artist, actor, writer, singer, tv personality', 'sportsperson, athlete, player, coach, referee',
            'student, pupil, schoolchild', ') only if no other occupation is given e.g. doctor/mother=code 6',
            'child, young person no other occupation given', 'villager or resident no other occupation given',
            'retired person, pensioner no other occupation given', 'criminal, suspect no other occupation given',
            'unemployed no other occupation given', 'other only as last resort & explain',
        ]

        col_start, end_index = 3, 114
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_s05(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'do not know', 'subject', 'spokesperson', 'expert or commentator', 'personal experience',
            'eye witness', 'personal opinion', 'other'
        ]

        col_start, end_index = 3, 34
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_s06(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'Victim', 'Not a victim',
        ]

        col_start, end_index = 3, 10
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_s07(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        options = ['yes', 'no']

        col_start, end_index = 3, 10
        while col_start < end_index:
            for option in options:
                option_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    option_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[option] = option_data
                col_start += 4

        return all_data

    def import_s08(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        options = ['yes', 'no']

        col_start, end_index = 3, 10
        while col_start < end_index:
            for option in options:
                option_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    option_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[option] = option_data
                col_start += 4

        return all_data

    def import_s09(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        options = ['yes', 'no', 'do not know']

        col_start, end_index = 3, 14
        while col_start < end_index:
            for option in options:
                option_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    option_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[option] = option_data
                col_start += 4

        return all_data

    def import_s10(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Reporter',
            ],
            medium='Print',
            col_start=3,
            end_index=6,
            row_end=122,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Presenter',
                'Reporter',
            ],
            medium='Radio',
            col_start=7,
            end_index=14,
            row_end=122,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Presenter',
                'Reporter',
            ],
            medium='Television',
            col_start=15,
            end_index=22,
            row_end=122,
        )

        return all_data

    def import_s11(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 30
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=121,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_s12(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 9, 7, 120),
            ]
        )

    def import_s13(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 10
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 4

        return all_data
    
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

    def _secondary_import_s17(self, data, medium, col_start, end_index):
        groups = ['reporter', 'subjects']
        medium_data = {}
        medium_data[medium] = {}
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                medium_data[medium][group] = group_data
                col_start += 4
            data[medium] = medium_data[medium]

    def import_s17(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._secondary_import_s17(
            data=data_2015,
            medium='internet',
            col_start=3,
            end_index=11,
        )

        n_data_2015 = {}
        data_2015['internet']['n'] = n_data_2015
        for col_start, col_end, row_start, row_end, col_heading_row in [
            (11, 11, 9, 122, 7),
        ]:
            self.slurp_table(
                self.ws,
                n_data_2015,
                col_start=col_start,
                col_end=col_end,
                row_start=row_start,
                row_end=row_end,
                col_heading_row=col_heading_row,
            )

        self._secondary_import_s17(
            data=data_2015,
            medium='twitter',
            col_start=23,
            end_index=30,
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

    def import_s19(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        data_2015['internet'] = {}
        col_start, end_index = 3, 30
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['internet'][group] = group_data
                col_start += 4

        data_2015['twitter'] = {}
        col_start, end_index = 33, 60
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['twitter'][group] = group_data
                col_start += 4

        return all_data

    def import_s20(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'not stated', 'royalty, monarch, deposed monarch, etc.',
            'government, politician, minister, spokesperson...', 'government employee, public servant, etc.',
            'police, military, para-military, militia, fire officer', 'academic expert, lecturer, teacher',
            'doctor, dentist, health specialist', 'health worker, social worker, childcare worker',
            'science/technology professional, engineer, etc.', 'media professional, journalist, film-maker, etc.',
            'lawyer, judge, magistrate, legal advocate, etc.', 'business person, exec, manager, stock broker...',
            'office or service worker, non-management worker', 'tradesperson, artisan, labourer, truck driver, etc.',
            'agriculture, mining, fishing, forestry', 'religious figure, priest, monk, rabbi, mullah, nun',
            'activist or worker in civil society org., ngo, trade union', 'sex worker',
            'celebrity, artist, actor, writer, singer, tv personality', 'sportsperson, athlete, player, coach, referee',
            'student, pupil, schoolchild', ') only if no other occupation is given e.g. doctor/mother=code 6',
            'child, young person no other occupation given', 'villager or resident no other occupation given',
            'retired person, pensioner no other occupation given', 'criminal, suspect no other occupation given',
            'unemployed no other occupation given', 'other only as last resort & explain',
        ]

        data_2015['internet'] = {}
        col_start, end_index = 3, 114
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['internet'][group] = group_data
                col_start += 4

        return all_data

    def import_s21(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'do not know', 'subject', 'spokesperson', 'expert or commentator', 'personal experience',
            'eye witness', 'personal opinion', 'other'
        ]

        data_2015['internet'] = {}
        col_start, end_index = 3, 34
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['internet'][group] = group_data
                col_start += 4

        return all_data

    def import_s22(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'victim', 'not a victim',
        ]

        data_2015['internet'] = {}
        col_start, end_index = 3, 10
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['internet'][group] = group_data
                col_start += 4

        return all_data

    def import_s23(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'yes', 'no',
        ]

        data_2015['internet'] = {}
        col_start, end_index = 3, 10
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['internet'][group] = group_data
                col_start += 4

        return all_data

    def import_s24(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        options = ['yes', 'no', 'do not know']

        data_2015['internet'] = {}
        col_start, end_index = 3, 14
        while col_start < end_index:
            for option in options:
                option_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    option_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['internet'][option] = option_data
                col_start += 4

        data_2015['twitter'] = {}
        col_start, end_index = 17, 28
        while col_start < end_index:
            for option in options:
                option_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    option_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['twitter'][option] = option_data
                col_start += 4

        return all_data

    def import_s25(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        data_2015['internet'] = {}
        col_start, end_index = 3, 30
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['internet'][group] = group_data
                col_start += 4

        data_2015['twitter'] = {}
        col_start, end_index = 33, 60
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=7,
                    row_start=9,
                    row_end=122,
                    row_heading_col=2,
                )
                data_2015['twitter'][group] = group_data
                col_start += 4

        return all_data

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

    def import_rs01(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        categories = ['presenter', 'reporter', 'subjects']

        col_start, end_index = 3, 14
        while col_start < end_index:
            for category in categories:
                category_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    category_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[category] = category_data
                col_start += 4

        return all_data

    def import_sr02(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 30
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_sr03(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'do not know', 'subject', 'spokesperson', 'expert or commentator', 'personal experience',
            'eye witness', 'personal opinion', 'other'
        ]

        col_start, end_index = 3, 34
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_sr04(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        options = ['yes', 'no', 'do not know']

        col_start, end_index = 3, 14
        while col_start < end_index:
            for option in options:
                option_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    option_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[option] = option_data
                col_start += 4

        return all_data

    def import_sr05(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Reporter',
            ],
            medium='Print',
            col_start=3,
            end_index=6,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Presenter',
                'Reporter',
            ],
            medium='Radio',
            col_start=7,
            end_index=14,
        )

        self._sheet_80_secondary_import(
            data=data_2015,
            groups=[
                'Presenter',
                'Reporter',
            ],
            medium='Television',
            col_start=15,
            end_index=22,
        )

        return all_data

    def import_sr06(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        groups = [
            'politics and government', 'economy', 'science and health', 'social and legal', 'crime and violence',
            'celebrity, arts and media, sports', 'other'
        ]

        col_start, end_index = 3, 30
        while col_start < end_index:
            for group in groups:
                group_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    group_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[group] = group_data
                col_start += 4

        return all_data

    def import_sr07(self, sheet_data):
        data_2015 = {}
        all_data = {2015: data_2015}

        genders = ['female', 'male']

        col_start, end_index = 3, 10
        while col_start < end_index:
            for gender in genders:
                gender_data = {}
                self.slurp_secondary_col_table(
                    self.ws,
                    gender_data,
                    col_start=col_start,
                    cols=2,
                    cols_per_group=2,
                    major_col_heading_row=6,
                    row_start=8,
                    row_end=16,
                    row_heading_col=2,
                )
                data_2015[gender] = gender_data
                col_start += 4

        return all_data

    def import_sr08(self, sheet_info):
        return self.import_grid(
            [
                (2015, 3, 9, 7, 15),
            ]
        )

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
