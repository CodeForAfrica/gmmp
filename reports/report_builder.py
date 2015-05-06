# Python
import StringIO

# 3rd Party
import xlsxwriter
from django_countries import countries

# Project
from reports.constants import *
from forms.models import (
    InternetNewsSheet,
    TwitterSheet,
    NewspaperSheet,
    TelevisionSheet,
    RadioSheet)

sheet_models = {
    'Internet News': InternetNewsSheet,
    'Print': NewspaperSheet,
    'Radio': RadioSheet,
    'Television': TelevisionSheet,
    'Twitter': TwitterSheet
}


class XLSXReportBuilder:
    def __init__(self, form):
        self.form = form
        self.countries = form.get_countries()
        self.gmmp_year = '2015'

    def build(self):
        """
        Generate an Excel spreadsheet and return it as a string.
        """
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)

        # Add generic sheets here.
        self.medium_per_country_worksheet(workbook)

        workbook.close()
        output.seek(0)

        return output.read()

    def medium_per_country_worksheet(self, wb):
        ws = wb.add_worksheet('Medium per country')

        ws.write(0, 0, 'Participating Countries in each Region')
        ws.write(1, 0, 'Breakdown of all media by country')

        # Is there a more efficient wat to do this?
        ws.write(5, 0, 'Region name here')

        row, col = 5, 1
        for country in self.countries:
            ws.write(row, col, dict(countries)[country])
            row += 1

        ws.write(3, 2, self.gmmp_year)

        row, col = 4, 2

        for media_type in MEDIA_TYPES:
            ws.write(row, col, media_type)
            col += 1

        row, col = 5, 2









