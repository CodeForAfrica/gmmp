# Python
import StringIO

# 3rd Party
import xlsxwriter
from django_countries import countries

# Project
from reports.constants import *


class XLSXReportBuilder:
    def __init__(self, form):
        self.form = form
        self.country = form.cleaned_data.get('country')
        self.gmmp_year = '2015'

    def build(self):
        """
        Generate an Excel spreadsheet and return it as a string.
        """
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)

        # Add generic sheets here.

        # Fix this check
        if self.country:
            self.medium_per_country_worksheet(workbook)

        workbook.close()
        output.seek(0)

        return output.read()

    def medium_per_country_worksheet(self, wb):
        import ipdb; ipdb.set_trace()
        ws = wb.add_worksheet('Medium per country')

        ws.write('A1', 'Participating Countries in each Region')
        ws.write('A2', 'Breakdown of all media by country')

        # Is there a more efficient wat to do this?
        ws.write(5,0, 'Region name here')
        ws.write(6,0, dict(countries)[self.country])

        ws.write(3, 1, self.gmmp_year)







