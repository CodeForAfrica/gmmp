# Python
import StringIO
from collections import OrderedDict

# 3rd Party
import xlsxwriter
from django_countries import countries
from django.db.models import Count

# Project

from forms.models import (
    InternetNewsSheet,
    TwitterSheet,
    NewspaperSheet,
    TelevisionSheet,
    RadioSheet)
from forms.modelutils import TOPICS


sheet_models = OrderedDict([
    ('Internet News', InternetNewsSheet),
    ('Print', NewspaperSheet),
    ('Radio', RadioSheet),
    ('Television', TelevisionSheet),
    ('Twitter', TwitterSheet)]
)


def p(n, d):
    """ Helper to calculate the percentage of n / d,
    returning 0 if d == 0.
    """
    if d == 0:
        return 0.0
    return float(n) / d


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

        # setup formats
        self.P = workbook.add_format()
        self.P.set_num_format(9)  # percentage

        # Add generic sheets here.
        self.ws_2_media_by_country(workbook)
        self.ws_4_topics_by_region(workbook)

        workbook.close()
        output.seek(0)

        return output.read()

    def ws_2_media_by_country(self, wb):
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

    def ws_4_topics_by_region(self, wb):
        ws = wb.add_worksheet('4 - Topics by region')

        ws.write(0, 0, 'Topics in the news by region')
        ws.write(1, 0, 'Breakdown of major news topics by region by medium')
        ws.write(3, 2, self.gmmp_year)

        # Is there a more efficient wat to do this?
        ws.write(5, 0, 'Region name here')

        row, col = 6, 1

        # row titles
        for i, topic in enumerate(TOPICS):
            id, topic = topic
            ws.write(row + i, col, unicode(topic))

        col += 1

        for media_type, model in sheet_models.iteritems():
            # column title
            ws.write(row - 2, col, media_type)
            ws.write(row - 1, col, "N")
            ws.write(row - 1, col + 1, "%")

            # row values
            rows = model.objects\
                    .values('topic')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('topic'))
            counts = {r['topic']: r['n'] for r in rows}
            total = sum(counts.itervalues())

            for i, topic in enumerate(TOPICS):
                id, topic = topic
                ws.write(row + i, col, counts.get(id, 0))
                ws.write(row + i, col + 1, p(counts.get(id, 0), total), self.P)

            col += 2
