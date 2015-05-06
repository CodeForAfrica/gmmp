# Python
import StringIO
from collections import OrderedDict

# 3rd Party
import xlsxwriter
from django_countries import countries

# Project

from forms.models import (
    InternetNewsSheet,
    TwitterSheet,
    NewspaperSheet,
    TelevisionSheet,
    RadioSheet)


sheet_models = OrderedDict([
    ('Internet News', InternetNewsSheet),
    ('Print', NewspaperSheet),
    ('Radio', RadioSheet),
    ('Television', TelevisionSheet),
    ('Twitter', TwitterSheet)]
)


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
        for name, sheet_model in sheet_models.iteritems():
            ws.write(row, col, name)
            col += 1

        col = 2
        for name, sheet_model in sheet_models.iteritems():
            row = 5
            for country in self.countries:
                data = sheet_model.objects.filter(country=country).count()
                ws.write(row, col, data)
                row += 1
            col += 1










