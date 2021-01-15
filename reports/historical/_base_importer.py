"""
Holds the base import class which holds methods which are
common to all year import classes. It also holds utility functions
"""
import re

from .canon import canon


def v(v):
    """
    Try to interpret a value as an percentage
    """
    try:
        basestring
    except NameError:
        basestring = str
    if not isinstance(v, basestring):
        return v

    m = re.match(r"^(\d+(\.\d+)?)(%)?$", v)
    if m:
        if not m.group(2):
            # int
            v = int(m.group(1))
        else:
            # float
            v = float(m.group(1))

        if m.group(3):
            v = v / 100.0
    return v


class BaseReportImporter(object):
    def __init__(self):
        self.ws = None

    def get_work_sheet(self, wb, sheet):
        for name in wb.sheetnames:
            if name == sheet.get("historical"):
                self.ws = wb[name]
        return self.ws

    def import_sheet(self, sheet):
        return getattr(self, "import_%s" % sheet.get("historical"))(sheet)

    def slurp_secondary_col_table(
        self,
        ws,
        data,
        col_start,
        cols_per_group,
        cols,
        row_end,
        row_start=5,
        major_col_heading_row=4,
        row_heading_col=5,
    ):
        """
        Get values from a table with two levels of column headings.

        eg.
            Major 1       | Major 2
            Col 1 | Col 2 | Col 1 | Col 2
        row1
        row2
        row3
        """
        for icol in range(col_start, col_start + cols * cols_per_group, cols_per_group):
            major_col_heading = canon(
                ws.cell(column=icol, row=major_col_heading_row).value
            )
            major_col_data = {}
            data[major_col_heading] = major_col_data

            self.slurp_table(
                ws,
                major_col_data,
                icol,
                icol + cols_per_group - 1,
                row_end,
                row_start=row_start,
                col_heading_row=major_col_heading_row + 1,
                row_heading_col=row_heading_col,
            )

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
        """
        Grab values from a simple table with column and row titles.

        eg.
            Cat 1 | Cat 2 | N
        row1
        row2
        row3
        """
        for icol in range(col_start, col_end + 1):
            col_heading = canon(ws.cell(column=icol, row=col_heading_row).value)
            if not col_heading:
                continue
            col_data = {}
            data[col_heading] = col_data

            for irow in range(row_start, row_end + 1):
                row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                col_data[row_heading] = v(ws.cell(column=icol, row=irow).value)

    def slurp_year_grouped_table(
        self,
        ws,
        all_data,
        col_start,
        cols_per_group,
        cols,
        row_end,
        row_start=5,
        year_heading_row=4,
        col_heading_row=3,
        row_heading_col=5,
        skip_years=[],
    ):
        """
        Slurp a table where each category contains a range of years.

        eg.
            Category 1      | Category 2      |
            2005 | 2010 | N | 2005 | 2010 | N |
        row1
        row2
        row3
        """
        for icol in range(col_start, col_start + cols * cols_per_group, cols_per_group):
            col_heading = canon(ws.cell(column=icol, row=col_heading_row).value)

            for iyear in range(icol, icol + cols_per_group):
                year = ws.cell(column=iyear, row=year_heading_row).value
                if year in ["N", "N-F"]:
                    year = 2010
                    effective_col_heading = canon("N")
                else:
                    year = int(year)
                    effective_col_heading = col_heading

                if year not in skip_years:
                    data = all_data.setdefault(year, {})
                    col_data = data.setdefault(effective_col_heading, {})

                    for irow in range(row_start, row_end + 1):
                        print("\n\n\n\n")
                        print(f"{year} {ws.cell(column=row_heading_col, row=irow).value}")
                        print("\n\n\n\n")
                        row_heading = canon(
                            ws.cell(column=row_heading_col, row=irow).value
                        )
                        col_data[row_heading] = v(ws.cell(column=iyear, row=irow).value)
