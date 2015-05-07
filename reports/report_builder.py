# Python
import StringIO
from collections import Counter

# Django
from django.core import urlresolvers
from django_countries import countries
from django.db.models import Count, FieldDoesNotExist
from django.contrib.sites.shortcuts import get_current_site

# 3rd Party
import xlsxwriter

# Project
from forms.models import NewspaperSheet, person_models, sheet_models, journalist_models
from forms.modelutils import (TOPICS, GENDER, SPACE, OCCUPATION, FUNCTION, SCOPE,
    YESNO, AGES, SOURCE, VICTIM_OF, SURVIVOR_OF, IS_PHOTOGRAPH, AGREE_DISAGREE,
    RETWEET, TV_ROLE, MEDIA_TYPES,
    CountryRegion)


def has_field(model, fld):
    try:
        model._meta.get_field(fld)
        return True
    except FieldDoesNotExist:
        return False


def p(n, d):
    """ Helper to calculate the percentage of n / d,
    returning 0 if d == 0.
    """
    if d == 0:
        return 0.0
    return float(n) / d

def get_regions():
    """
    Return a list of (id, region_name) tuples which exists in the db
    """
    country_regions = CountryRegion.objects\
                        .values('region')\
                        .exclude(region='Unmapped')
    regions = set(item['region'] for item in country_regions)
    return [(i, region) for i, region in enumerate(regions)]

class XLSXDataExportBuilder():
    def __init__(self, request):
        self.domain = "http://%s" % get_current_site(request).domain


    def build(self):
        """
        Generate an Excel spreadsheet and return it as a string.
        """
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)

        for model in sheet_models.itervalues():
            self.create_sheet_export(model, workbook)

        for model in person_models.itervalues():
            self.create_person_export(model, workbook)

        for model in journalist_models.itervalues():
            self.create_journalist_export(model, workbook)

        workbook.close()
        output.seek(0)

        return output.read()


    def create_sheet_export(self, model, wb):
        ws = wb.add_worksheet(model._meta.object_name)
        obj_list = model.objects.all()
        row, col = 0, 0
        exclude_fields = ['monitor', 'url_and_multimedia', 'time_accessed', 'country_region']
        fields = [field for field in model._meta.fields if not field.name in exclude_fields]

        for i, field in enumerate(fields):
            ws.write(row, col+i, unicode(field.name))
        ws.write(row, col+i+1, unicode('edit_url'))

        row += 1
        col = 0

        for y, obj in enumerate(obj_list):
            for x, field in enumerate(fields):
                # Certain fields are 1-indexed
                if field.name == 'country':
                    ws.write(row+y, col+x, getattr(obj, field.name).code)
                elif field.name == 'topic':
                    ws.write(row+y, col+x, unicode(TOPICS[getattr(obj, field.name)-1][1]))
                elif field.name == 'scope':
                    ws.write(row+y, col+x, unicode(SCOPE[getattr(obj, field.name)-1][1]))
                elif field.name == 'person_secondary':
                    ws.write(row+y, col+x, unicode(SOURCE[getattr(obj, field.name)][1]))
                elif field.name == 'inequality_women':
                    ws.write(row+y, col+x, unicode(AGREE_DISAGREE[getattr(obj, field.name)-1][1]))
                elif field.name == 'stereotypes':
                    ws.write(row+y, col+x, unicode(AGREE_DISAGREE[getattr(obj, field.name)-1][1]))
                elif field.name == 'space':
                    ws.write(row+y, col+x, unicode(SPACE[getattr(obj, field.name)-1][1]))
                elif field.name == 'retweet':
                    ws.write(row+y, col+x, unicode(RETWEET[getattr(obj, field.name)-1][1]))
                else:
                    ws.write(row+y,col+x, getattr(obj, field.name))
            change_url = urlresolvers.reverse(
                'admin:%s_%s_change' % (
                    obj._meta.app_label,
                    obj._meta.model_name),
                args=(obj.id,))
            ws.write_url(row+y, col+x+1, "%s%s" % (self.domain, change_url))


    def create_person_export(self, model, wb):
        ws = wb.add_worksheet(model._meta.object_name)
        obj_list = model.objects.all().prefetch_related(model.sheet_name())
        row, col = 0, 0
        exclude_fields = []
        fields = [field for field in model._meta.fields if not field.name in exclude_fields]

        for i, field in enumerate(fields):
            ws.write(row, col+i, unicode(field.name))
        ws.write(row, col+i+1, unicode('edit_url'))

        row += 1
        col = 0

        for y, obj in enumerate(obj_list):
            for x, field in enumerate(fields):
                # Certain fields are 1-indexed
                if field.name == 'sex':
                    ws.write(row+y, col+x, unicode(GENDER[getattr(obj, field.name)-1][1]))
                elif field.name == 'age':
                    ws.write(row+y, col+x, unicode(AGES[getattr(obj, field.name)][1]))
                elif field.name == 'occupation':
                    ws.write(row+y, col+x, unicode(OCCUPATION[getattr(obj, field.name)][1]))
                elif field.name == 'function':
                    ws.write(row+y, col+x, unicode(FUNCTION[getattr(obj, field.name)][1]))
                elif field.name == 'victim_of' and not getattr(obj, field.name) == None:
                    ws.write(row+y, col+x, unicode(VICTIM_OF[getattr(obj, field.name)][1]))
                elif field.name == 'survivor_of' and not getattr(obj, field.name) == None:
                    ws.write(row+y, col+x, unicode(SURVIVOR_OF[getattr(obj, field.name)][1]))
                elif field.name == 'is_photograph':
                    ws.write(row+y, col+x, unicode(IS_PHOTOGRAPH[getattr(obj, field.name)-1][1]))
                elif field.name == 'space':
                    ws.write(row+y, col+x, unicode(SPACE[getattr(obj, field.name)-1][1]))
                elif field.name == 'retweet':
                    ws.write(row+y, col+x, unicode(RETWEET[getattr(obj, field.name)-1][1]))
                elif field.name == obj.sheet_name():
                    ws.write(row+y, col+x, getattr(obj, field.name).id)
                    # Get the parent model and id for building the edit link
                    parent_model = field.related.parent_model
                    parent_id = getattr(obj, field.name).id
                else:
                    ws.write(row+y,col+x, getattr(obj, field.name))
            # Write link to end of row
            change_url = urlresolvers.reverse(
                'admin:%s_%s_change' % (
                    parent_model._meta.app_label,
                    parent_model._meta.model_name),
                args=(parent_id,))
            ws.write_url(row+y, col+x+1, "%s%s" % (self.domain, change_url))


    def create_journalist_export(self, model, wb):
        ws = wb.add_worksheet(model._meta.object_name)
        obj_list = model.objects.all().prefetch_related(model.sheet_name())
        row, col = 0, 0
        exclude_fields = []
        fields = [field for field in model._meta.fields if not field.name in exclude_fields]

        for i, field in enumerate(fields):
            ws.write(row, col+i, unicode(field.name))
        ws.write(row, col+i+1, unicode('edit_url'))

        row += 1
        col = 0

        for y, obj in enumerate(obj_list):
            for x, field in enumerate(fields):
                if field.name == 'sex':
                    ws.write(row+y, col+x, unicode(GENDER[getattr(obj, field.name)-1][1]))
                elif field.name == 'age' and not getattr(obj, field.name) == None:
                    ws.write(row+y, col+x, unicode(AGES[getattr(obj, field.name)][1]))
                elif field.name == obj.sheet_name():
                    ws.write(row+y, col+x, getattr(obj, field.name).id)
                    # Get the parent model and id for building the edit link
                    parent_model = field.related.parent_model
                    parent_id = getattr(obj, field.name).id
                else:
                    ws.write(row+y,col+x, getattr(obj, field.name))
            # Write link to end of row
            change_url = urlresolvers.reverse(
                'admin:%s_%s_change' % (
                    parent_model._meta.app_label,
                    parent_model._meta.model_name),
                args=(parent_id,))
            ws.write_url(row+y, col+x+1, "%s%s" % (self.domain, change_url))


class XLSXReportBuilder:
    def __init__(self, form):
        self.form = form
        self.countries = form.get_countries()
        self.regions = get_regions()
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
        self.ws_1_media_by_region(workbook)
        self.ws_2_media_by_country(workbook)
        self.ws_4_topics_by_region(workbook)
        self.ws_7_sex_by_media(workbook)
        self.ws_8_scope_by_source_sex(workbook)
        self.ws_9_topic_by_source_sex(workbook)
        self.ws_10_topic_by_space(workbook)
        self.ws_11_topic_by_gender_equality_reference(workbook)
        self.ws_13_topic_by_journalist_sex(workbook)
        self.ws_14_source_occupation_by_sex(workbook)
        self.ws_15_subject_function_by_sex(workbook)


        workbook.close()
        output.seek(0)

        return output.read()

    def ws_1_media_by_region(self, wb):
        ws = wb.add_worksheet('1 - Medium by region')

        self.write_headers(ws, 'Participating Countries', 'Breakdown of all media by region')

        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            region_field = 'country_region__region'
            rows = model.objects\
                    .values('country_region__region')\
                    .exclude(country_region__region='Unmapped')\
                    .annotate(n=Count('id'))
            for row in rows:
                if row['country_region__region'] is not None:
                    # Get media and region id's to assign to counts
                    media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                    region_id = [region[0] for region in self.regions if region[1] == row['country_region__region']][0]

                    counts.update({(media_id, region_id): row['n']})
                # counts.update({(media_type, r[region]): r['n'] for r in rows if r[region] is not None})

        self.tabulate(ws, counts, MEDIA_TYPES, self.regions, row_perc=True)


    def ws_2_media_by_country(self, wb):
        ws = wb.add_worksheet('2 - Medium by country')

        ws.write(0, 0, 'Participating Countries in each Region')
        ws.write(1, 0, 'Breakdown of all media by country')
        ws.write(3, 2, self.gmmp_year)

        ws.write(5, 0, 'Region name here')

        row, col = 6, 1

        # row headings
        for i, country in enumerate(self.countries):
            # Is this the best way to do this?
            ws.write(row + i, col, dict(countries)[country])

        col += 1

        counts = Counter()

        for media_type, model in sheet_models.iteritems():
            # row values
            rows = model.objects\
                    .values('country')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('country'))

            counts.update({(media_type, r['country']): r['n'] for r in rows})

        row_totals = {}
        for country in self.countries:
            row_totals[country] = sum(counts.get((media_type, country), 0) for media_type, m in sheet_models.iteritems())

        for media_type, model in sheet_models.iteritems():
            # column title
            ws.write(row - 2, col, media_type)
            ws.write(row - 1, col, "N")
            ws.write(row - 1, col + 1, "%")

            # row values
            for i, country in enumerate(self.countries):
                c = counts.get((media_type, country), 0)
                ws.write(row + i, col, c)
                ws.write(row + i, col + 1, p(c, row_totals[country]), self.P)

            col += 2

    def ws_4_topics_by_region(self, wb):
        ws = wb.add_worksheet('4 - Topics by region')

        ws.write(0, 0, 'Topics in the news by region')
        ws.write(1, 0, 'Breakdown of major news topics by region by medium')
        ws.write(3, 2, self.gmmp_year)

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

    def ws_7_sex_by_media(self, wb):
        ws = wb.add_worksheet('7 - Sex by media')

        ws.write(0, 0, 'Women in the news (sources) by medium')
        ws.write(1, 0, 'Breakdown by sex of all mediums')
        ws.write(3, 2, self.gmmp_year)

        row, col = 6, 1

        # row titles
        for i, gender in enumerate(GENDER):
            id, gender = gender
            ws.write(row + i, col, unicode(gender))

        col += 1

        for media_type, model in sheet_models.iteritems():
            # column title
            ws.write(row - 2, col, media_type)
            ws.write(row - 1, col, "N")
            ws.write(row - 1, col + 1, "%")

            # row values
            sex = '%s__sex' % model.person_field_name()
            rows = model.objects\
                    .values(sex)\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))
            counts = {r[sex]: r['n'] for r in rows if r[sex] is not None}
            total = sum(counts.itervalues())

            for i, topic in enumerate(GENDER):
                id, topic = topic
                ws.write(row + i, col, counts.get(id, 0))
                ws.write(row + i, col + 1, p(counts.get(id, 0), total), self.P)

            col += 2

    def ws_8_scope_by_source_sex(self, wb):
        ws = wb.add_worksheet('8 - Scope by source sex')
        self.write_headers(
            ws,
            'Sex of news subjects (sources) inlocal,national,sub-regional/regional, foreign/intnl news',
            'Breakdown by sex local,national,sub-regional/regional, intnl news')

        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            if 'scope' in model._meta.get_all_field_names():
                sex = '%s__sex' % model.person_field_name()
                rows = model.objects\
                        .values(sex, 'scope')\
                        .filter(country__in=self.countries)\
                        .annotate(n=Count('id'))
                counts.update({(r[sex], r['scope']): r['n'] for r in rows if r[sex] is not None})

        self.tabulate(ws, counts, GENDER, SCOPE, row_perc=True)

    def ws_9_topic_by_source_sex(self, wb):
        ws = wb.add_worksheet('9 - Topic by source sex')

        ws.write(0, 0, 'Sex of news subjects in different story topics')
        ws.write(1, 0, 'Breakdown of topic by sex')
        ws.write(3, 2, self.gmmp_year)

        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            sex = '%s__sex' % model.person_field_name()
            rows = model.objects\
                    .values(sex, 'topic')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))
            counts.update({(r[sex], r['topic']): r['n'] for r in rows if r[sex] is not None})

        self.tabulate(ws, counts, GENDER, TOPICS, row_perc=True)

    def ws_10_topic_by_space(self, wb):

        ws = wb.add_worksheet('10 - Topic by space')

        ws.write(0, 0, 'Space allocated to major topics in Newspapers')
        ws.write(1, 0, 'Breakdown by major topic by space (q.4) in newspapers')
        ws.write(3, 2, self.gmmp_year)

        # Calculate row values for column
        rows = NewspaperSheet.objects\
                .values('space', 'topic')\
                .filter(country__in=self.countries)\
                .annotate(n=Count('id'))
        counts = {(r['space'], r['topic']): r['n'] for r in rows}

        self.tabulate(ws, counts, SPACE, TOPICS, row_perc=True)

    def ws_11_topic_by_gender_equality_reference(self, wb):

        ws = wb.add_worksheet('11 - Topic by reference to gender equality')

        ws.write(0, 0, 'Stories making reference to issues of gender equality/inequality, legislation, policy by major topic')
        ws.write(1, 0, 'Breakdown by major topic by reference to gender equality/human rights/policy ')
        ws.write(3, 2, self.gmmp_year)

        row, col = 6, 1

        # row titles
        for i, topic in enumerate(TOPICS):
            id, topic = topic
            ws.write(row + i, col, unicode(topic))

        col += 1



    def ws_13_topic_by_journalist_sex(self, wb):
        ws = wb.add_worksheet('13 - Topic by reporter sex')

        ws.write(0, 0, 'Sex of reporter in different story topics')
        ws.write(1, 0, 'Breakdown of topic by reporter sex')
        ws.write(3, 2, self.gmmp_year)

        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            sex = '%s__sex' % model.journalist_field_name()
            rows = model.objects\
                    .values(sex, 'topic')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))
            counts.update({(r[sex], r['topic']): r['n'] for r in rows if r[sex] is not None})

        self.tabulate(ws, counts, GENDER, TOPICS, row_perc=True)

    def ws_14_source_occupation_by_sex(self, wb):
        ws = wb.add_worksheet('14 - Source occupation by sex')

        ws.write(0, 0, 'Position or occupation of news sources, by sex')
        ws.write(1, 0, 'Breakdown of new sources by occupation and sex')
        ws.write(3, 2, self.gmmp_year)

        counts = Counter()
        for model in person_models.itervalues():
            # some models don't have an occupation
            if not has_field(model, 'occupation'):
                continue

            rows = model.objects\
                    .values('sex', 'occupation')\
                    .filter(**{model.sheet_name() + '__country__in': self.countries})\
                    .annotate(n=Count('id'))
            counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, OCCUPATION, row_perc=True)

    def ws_15_subject_function_by_sex(self, wb):
        ws = wb.add_worksheet('15 - Subject function by sex')

        ws.write(0, 0, 'News subject''s Function in news story, by sex')
        ws.write(1, 0, 'Breakdown by sex and function')
        ws.write(3, 2, self.gmmp_year)

        counts = Counter()

        for model in person_models.itervalues():
            # some models don't have a function
            if not has_field(model, 'function'):
                continue

            rows = model.objects\
                    .values('sex', 'function')\
                    .filter(**{model.sheet_name() + '__country__in': self.countries})\
                    .annotate(n=Count('id'))
            counts.update({(r['sex'], r['function']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, FUNCTION, row_perc=True)


    # -------------------------------------------------------------------------------
    # Helper functions
    #
    def write_headers(self, ws, title, description):
        """
        Write the headers to the worksheet
        """
        ws.write(0, 0, title)
        ws.write(1, 0, description)
        ws.write(3, 2, self.gmmp_year)


    def tabulate(self, ws, counts, cols, rows, row_perc=False):
        """ Emit a table.

        :param ws: worksheet to write to
        :param dict counts: dict from `(col_id, row_id)` tuples to count for that combination.
        :param list cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param list rows: list of `(row_id, row_title)` tuples of row ids and titles
        :param bool row_perc: should percentages by calculated by row instead of column (default: False)
        """
        r, c = 6, 1

        if row_perc:
            # we'll need percentage by rows
            row_totals = {}
            for row_id, row_title in rows:
                row_totals[row_id] = sum(counts.get((col_id, row_id), 0) for col_id, _ in cols)  # noqa

        # row titles
        for i, row in enumerate(rows):
            row_id, row_title = row
            ws.write(r + i, c, unicode(row_title))

        c += 1

        # values, written by column
        for col_id, col_title in cols:
            # column title
            ws.write(r - 2, c, unicode(col_title))
            ws.write(r - 1, c, "N")
            ws.write(r - 1, c + 1, "%")

            if not row_perc:
                # column totals
                total = sum(counts.itervalues())

            # row values for this column
            for i, row in enumerate(rows):
                row_id, row_title = row

                if row_perc:
                    # row totals
                    total = row_totals[row_id]

                n = counts.get((col_id, row_id), 0)
                ws.write(r + i, c, n)
                ws.write(r + i, c + 1, p(n, total), self.P)

            c += 2
