from .canon import canon
from ._base_importer import BaseReportImporter, v


class GMMP2010ReportImporter(BaseReportImporter):
    """
    Holds the methods that handles importing the GMMP 2010 final report
    """

    def __init__(self):
        BaseReportImporter.__init__(self)

    def import_1F(self, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(self.ws, data, col_start=15, col_end=18, row_end=12)

        return all_data

    def import_2aF(self, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(
            self.ws, data, col_start=15, col_end=17, row_start=5, row_end=12
        )

        return all_data

    def import_2F(self, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(
            self.ws, data, col_start=15, col_end=18, row_start=6, row_end=114
        )

        return all_data

    def import_3aF(self, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(
            self.ws, data, col_start=6, col_end=13, row_end=11, col_heading_row=3
        )

        return all_data

    def import_3bF(self, sheet_info):
        all_data = {}

        for icol in [6, 11, 16, 21, 26, 31, 36, 41]:
            data = {}
            self.slurp_year_grouped_table(
                self.ws,
                data,
                col_start=icol,
                cols=1,
                cols_per_group=5,
                year_heading_row=3,
                col_heading_row=2,
                row_start=4,
                row_end=11,
                skip_years=[1995, 2000, 2005],
            )

            year = list(data.keys())[0]
            all_data.setdefault(year, {})

            for items in data.values():
                keys = list(items.keys())
                keys.remove("n")
                key = keys[0]

                n_values = items["n"]
                p_values = items[key]

                for k, _ in list(p_values.items()):
                    p_values[k] = [p_values[k], n_values[k]]

                del items["n"]
                all_data[year][key] = {"female": items[key]}

        return all_data

    def import_9aF(self, sheet_info):
        data = dict()
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=4,
            col_heading_row=3,
            row_start=4,
            row_end=12,
            row_heading_col=5,
        )

        return data

    def import_9bF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=3,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=4,
            row_end=5,
        )
        return data

    def import_9cF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=5,
            row_end=8,
        )
        return data

    def import_9dF(self, sheet_info):
        data = {}
        all_data = {2010: data}

        col_heading = canon("Female")
        col_data = {}
        data[col_heading] = col_data

        for irow in range(4, 55):
            row_heading = canon(self.ws.cell(column=5, row=irow).value)
            col_data[row_heading] = v(self.ws.cell(column=8, row=irow).value)

        return all_data

    def import_9eF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=5,
            row_end=30,
        )
        return data

    def import_9fF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=5,
            row_end=12,
        )
        return data

    def import_9gF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=2,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=5,
            row_end=12,
        )
        return data

    def import_9hF(self, sheet_info):
        data = {}
        for col_start, cols_per_group in [(6, 4), (11, 2)]:
            self.slurp_year_grouped_table(
                self.ws,
                data,
                col_start=col_start,
                cols=1,
                cols_per_group=cols_per_group,
                year_heading_row=3,
                col_heading_row=2,
                row_start=4,
                row_end=5,
                row_heading_col=5,
            )
        return data

    def import_9kF(self, sheet_info):
        data = {}
        all_data = {2010: data}
        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=17,
            cols_per_group=3,
            cols=2,
            row_start=6,
            row_end=7,
            major_col_heading_row=4,
            row_heading_col=4,
        )
        return all_data

    def import_10bF(self, sheet_info):
        all_data = {}
        self.slurp_year_grouped_table(
            self.ws,
            all_data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=4,
            row_end=11,
        )
        return all_data

    def import_12dF(self, sheet_info):
        data = {}
        all_data = {2010: data}

        col_heading = canon("Female")
        col_data = {}
        data[col_heading] = col_data

        for irow in range(4, 55):
            row_heading = canon(self.ws.cell(column=5, row=irow).value)
            col_data[row_heading] = v(self.ws.cell(column=9, row=irow).value)

        return all_data

    def import_13bF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=4,
            year_heading_row=3,
            col_heading_row=2,
            row_start=5,
            row_end=9,
            skip_years=[1995],
        )
        return data

    def import_14F(self, sheet_info):
        all_data = {}

        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=5,
            row_end=11,
            skip_years=[1995, 2000],
        )
        for k, v in data.items():
            all_data.setdefault(k, {})[
                canon(
                    "Anchor, announcer or presenter: Usually in the television studio"
                )
            ] = v

        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=23,
            col_heading_row=22,
            row_start=25,
            row_end=31,
            skip_years=[1995, 2000],
        )
        for k, v in data.items():
            all_data.setdefault(k, {})[
                canon(
                    """
                    Reporter: Usually outside the studio. Include reporters who do not appear on screen, 
                    but whose voice is heard (e.g. as voice-over).
                    """
                )
            ] = v

        return all_data

    def import_15aF(self, sheet_info):
        data = {}

        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=2,
            cols_per_group=5,
            year_heading_row=5,
            col_heading_row=4,
            row_start=7,
            row_end=8,
            skip_years=[1995, 2000],
        )

        return data

    def import_15bF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=1,
            cols_per_group=5,
            year_heading_row=4,
            col_heading_row=3,
            row_start=5,
            row_end=56,
            skip_years=[1995, 2000, 2005],
        )
        return data

    def import_15cF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=8,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=4,
            row_end=55,
            skip_years=[1995, 2000, 2005],
        )
        return data

    def import_16cF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=2,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=4,
            row_end=11,
            skip_years=[1995, 2000, 2005],
        )
        return data

    def import_16dF(self, sheet_info):
        data = {}
        self.slurp_year_grouped_table(
            self.ws,
            data,
            col_start=6,
            cols=2,
            cols_per_group=5,
            year_heading_row=3,
            col_heading_row=2,
            row_start=4,
            row_end=11,
            skip_years=[1995, 2000, 2005],
        )
        return data

    def import_16eF(self, sheet_info):
        data = {}
        for col_start, cols_per_group, skip_years in [
            (6, 5, [1995, 2000, 2005]),
            (11, 2, []),
        ]:
            self.slurp_year_grouped_table(
                self.ws,
                data,
                col_start=col_start,
                cols=1,
                cols_per_group=cols_per_group,
                year_heading_row=3,
                col_heading_row=2,
                row_start=4,
                row_end=55,
                row_heading_col=5,
                skip_years=skip_years,
            )
        return data

    def import_18cF(self, sheet_info):
        all_data = {}

        for year, col_start, col_end in [(2005, 10, 11), (2010, 12, 14)]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_start=6,
                row_end=11,
                col_heading_row=4,
            )

        return all_data

    def import_18dF(self, sheet_info):
        all_data = {}

        col_heading = canon("radio")
        col_data = {}
        all_data[2010] = {col_heading: col_data}
        self.slurp_table(
            self.ws,
            col_data,
            col_start=12,
            col_end=13,
            col_heading_row=4,
            row_start=6,
            row_end=11,
        )

        col_heading = canon("television")
        for year, col_start, col_end in [(2005, 18, 19), (2010, 20, 22)]:
            col_data = {}

            if year in all_data:
                all_data[year][col_heading] = col_data
            else:
                all_data[year] = {col_heading: col_data}

            self.slurp_table(
                self.ws,
                col_data,
                col_start=col_start,
                col_end=col_end,
                col_heading_row=4,
                row_start=6,
                row_end=11,
            )

        return all_data

    def import_20aF(self, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=48,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=3,
            row_start=7,
            row_end=31,
        )
        return all_data

    def import_20bF(self, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=42,
            cols=6,
            cols_per_group=2,
            major_col_heading_row=3,
            row_start=6,
            row_end=11,
        )
        return all_data

    def import_20fF(self, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_secondary_col_table(
            self.ws,
            data,
            col_start=48,
            cols=7,
            cols_per_group=2,
            major_col_heading_row=3,
            row_start=7,
            row_end=31,
        )
        return all_data

    def import_19bF(self, sheet_info):
        all_data = {}

        for year, col_start, col_end in [(2005, 10, 11), (2010, 12, 14)]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_start=6,
                row_end=13,
                col_heading_row=4,
            )

        return all_data

    def import_20gF(self, sheet_info):
        all_data = {}

        for year, col_start, col_end in [(2000, 8, 9), (2005, 10, 11), (2010, 12, 13)]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_start=7,
                row_end=7,
                col_heading_row=4,
            )

        return all_data

    def import_20hF(self, sheet_info):
        all_data = {}

        for year, col_start, col_end in [(2000, 8, 9), (2005, 10, 11), (2010, 12, 14)]:
            data = {}
            all_data[year] = data
            self.slurp_table(
                self.ws,
                data,
                col_start=col_start,
                col_end=col_end,
                row_start=6,
                row_end=7,
                col_heading_row=4,
            )

        return all_data
