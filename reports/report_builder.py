# Python
import io
from collections import Counter, OrderedDict
import logging
import datetime

# Django
from django.conf import settings
from django.db import connection
from django.db.models import Count, FieldDoesNotExist

# 3rd Party
from django_countries import countries
import xlsxwriter

# Project
from forms.models import (
    NewspaperPerson, TelevisionJournalist,
    person_models, sheet_models, journalist_models,
    tm_person_models, tm_sheet_models, tm_journalist_models,
    dm_person_models, dm_sheet_models, dm_journalist_models, all_models,
    broadcast_journalist_models)
from forms.modelutils import (TOPICS, GENDER, SPACE, OCCUPATION, FUNCTION, SCOPE,
    YESNO, AGES, AGES_PEOPLE_IN_THE_NEWS, SOURCE, VICTIM_OF, SURVIVOR_OF, IS_PHOTOGRAPH, AGREE_DISAGREE,
    RETWEET, TV_ROLE, MEDIA_TYPES, TM_MEDIA_TYPES, DM_MEDIA_TYPES, CountryRegion,
    TV_ROLE_ANNOUNCER, TV_ROLE_REPORTER, REPORTERS)
from .report_details import *  # noqa
from reports.models import Weights
from reports.historical import Historical, canon
from reports.report_csv import (generate_csv, ws_05_csv, ws_09_csv,
    ws_15_csv, ws_28b_csv, ws_28c_csv, ws_30_csv, ws_38_csv, ws_41_csv, ws_47_csv, ws_48_csv, ws_83_csv,
    ws_85_csv, ws_92_csv, )

SHEET_MEDIA_GROUPS = [
    (TM_MEDIA_TYPES, tm_sheet_models),
    (DM_MEDIA_TYPES, dm_sheet_models)
]

PERSON_MEDIA_GROUPS = [
    (TM_MEDIA_TYPES, tm_person_models),
    (DM_MEDIA_TYPES, dm_person_models)
]

JOURNO_MEDIA_GROUPS = [
    (TM_MEDIA_TYPES, tm_journalist_models),
    (DM_MEDIA_TYPES, dm_journalist_models)
]

media_split = [
    "Print, Radio, Television",
    "Internet",
    "Twitter"
]

COUNTRY_RECODES = {
    u'QM': u'BE',  # Belgium - French -> Belgium
    u'QN': u'BE',  # Belgium - Flemish -> Belgium
    u'QO': u'GB',  # England -> United Kingdom
    u'QP': u'GB',  # Northern Ireland-> United Kingdom
    u'QQ': u'GB',  # Scotland -> United Kingdom
    u'QR': u'GB',  # Wales -> United Kingdom
}


# =================
# General utilities
# =================

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

def clean_title(text):
    """
    Return the string passed in stripped of its numbers and parentheses
    Except for the DRC. Of course.
    """
    text = str(text)
    if text != "Congo (the Democratic Republic of the)":
        return text[text.find(')')+1:].lstrip()
    return text

def get_sheet_model_name_field(media_type):
    if media_type == "Internet":
        return "website_name"
    elif media_type == "Twitter":
        return "media_name"
    elif media_type == "Print":
        return "newspaper_name"
    elif media_type == "Television":
        return "channel"
    elif media_type == "Radio":
        return "channel"

def sheet_name_to_num(sheet):
    """
    Helper function to convert sheet name to it's numerical equivalent taking
    into account different type of sheets.
    e.g. returns 10 for ws_10, 10.1 for ws_10b, and 202 for ws_s02.
    Sheets are banded: 0 - 199 normal sheets, 200 - 399 s sheets, and 400+ for
    sr sheets.
    """
    stripped_sheet = sheet.strip("wsrbc_")
    try:
        num = int(stripped_sheet, 10)
    except ValueError:
       num = 0

    if sheet.endswith("b"):
        num += 0.1
    if sheet.endswith("c"):
        num += 0.2
    if sheet.startswith("ws_sr"):
        return 400 + num
    
    if sheet.startswith("ws_s"):
        return 200 + num
    
    return num


class XLSXReportBuilder:
    def __init__(self, form):
        from reports.views import CountryForm, RegionForm

        self.form = form
        self.log = logging.getLogger(__name__)

        if isinstance(form, CountryForm):
            self.countries = form.filter_countries()
            self.regions = get_country_region(form.cleaned_data['country'])
            self.report_type = 'country'
        elif isinstance(form, RegionForm):
            region = [name for i, name in form.get_form_regions() if str(i) == form.cleaned_data['region']][0]
            self.countries = get_region_countries(region)
            self.regions = [(0, region)]
            self.report_type = 'region'
        else:
            self.countries = get_countries()
            self.regions = get_regions()
            self.report_type = 'global'

        self.country_list = [code for code, name in self.countries]
        self.all_regions = add_transnational_to_regions(self.regions) if self.report_type == 'global' else self.regions
        self.all_region_list = [name for id, name in self.all_regions]
        self.region_list = [name for id, name in self.regions]

        if self.report_type == 'global':
            self.recode_countries()

        # Various utilities used for displaying details
        self.male_female = [(id, value) for id, value in GENDER if id in [1, 2]]
        self.male_female_ids = [id for id, value in self.male_female]
        self.female = [(id, value) for id, value in GENDER if id == 1]
        self.female_ids = [id for id, value in self.female]
        self.yes = [(id, value) for id, value in YESNO if id == 'Y']

        self.current_year = settings.REPORTS_CURRENT_YEAR
        self.historical_year = settings.REPORTS_HISTORICAL_YEAR

        self.historical = Historical()
        self.historical.load()

    def recode_countries(self):
        # squash recoded countries
        self.countries = [(c, n) for c, n in self.countries if c not in COUNTRY_RECODES]
        # add GB and Belgium
        self.countries.append((u'BE', u'Belgium - French and Flemish'))
        self.countries.append((u'GB', u'United Kingdom - England, Northern Ireland, Scotland and Wales'))
        self.countries.sort(key=lambda p: p[1])

    def build(self):
        """
        Generate an Excel spreadsheet and return it as a string.
        """
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # setup formats
        self.heading = workbook.add_format(FORMATS['heading'])

        self.col_heading = workbook.add_format(FORMATS['col_heading'])
        self.col_heading_def = workbook.add_format(FORMATS['col_heading_def'])

        self.sec_col_heading = workbook.add_format(FORMATS['sec_col_heading'])
        self.sec_col_heading_def = workbook.add_format(FORMATS['sec_col_heading_def'])

        self.label = workbook.add_format(FORMATS['label'])

        self.N = workbook.add_format(FORMATS['N'])
        self.P = workbook.add_format(FORMATS['P'])

        sheets = list(WS_INFO.keys())

        # choose only those suitable for this report type
        report_type_sheets = []
        for sheet in sheets:
            sheet_info = WS_INFO[sheet].get(self.historical_year)
            if sheet_info and ("reports" in sheet_info and self.report_type in sheet_info["reports"]):
                report_type_sheets.append(sheet)

        sheets = sorted(report_type_sheets, key=sheet_name_to_num)

        self.write_key_sheet(workbook, sheets)

        self.write_aggregate_sheet(workbook)

        for sheet in sheets:
            sheet_info = WS_INFO[sheet][self.historical_year]
            ws = workbook.add_worksheet(sheet_info['name'])
            self.write_headers(ws, sheet_info['title'], sheet_info['desc'])
            self.log.info("Building sheet %s", sheet)
            getattr(self, sheet)(ws)
            self.log.info("Completed sheet %s", sheet)

        if not settings.DEBUG:
            self.write_raw_data_sheets(workbook)

        workbook.close()
        output.seek(0)

        return output.read()

    def write_key_sheet(self, workbook, sheets):
        ws = workbook.add_worksheet('Key')

        ws.write(0, 0, 'Key to Query Sheets', self.heading)

        ws.write(2, 0, 'N')
        ws.write(2, 1, 'number of items (weighted)')
        ws.write(3, 0, 'N (raw)')
        ws.write(3, 1, 'number of items (NOT weighted)')

        ws.write(5, 0, 'Number', self.col_heading)
        ws.write(5, 1, 'Number in 2015 Report', self.col_heading)
        ws.write(5, 2, 'Title', self.col_heading)
        ws.write(5, 3, 'Description', self.col_heading)

        for i, sheet in enumerate(sheets):
            sheet_info = WS_INFO[sheet][self.historical_year]
            ws.write(6 + i, 0, sheet_info['name'])
            ws.write(6 + i, 1, sheet_info['title'])
            ws.write(6 + i, 1, sheet_info.get('historical', ''))
            ws.write(6 + i, 2, sheet_info['desc'])


    def write_aggregate_sheet(self, workbook):
        ws = workbook.add_worksheet('Aggregates')
        c = 1
        ws.write(0, 0, 'Total amount of sheets, sources and reporters by country and media type.')
        for data_type, models in all_models.items():
            r = 3
            ws.write(r-1, c+1, data_type)
            for i, col in enumerate(MEDIA_TYPES):
                ws.write(r, c+1+i, clean_title(col[1]), self.col_heading)
                ws.write(r + 1, c+1+i, "N (raw)")

            r = 6
            for region_id, region in self.regions:
                counts = Counter()
                for media_type, model in models.items():
                    if data_type == 'Sheets':
                        country_field = 'country'
                    else:
                        country_field = model.sheet_name() + '__country'
                    rows = model.objects\
                            .values(country_field)\
                            .filter(**{country_field + '__in': self.country_list})\
                            .annotate(n=Count('id'))

                    for row in rows:
                        if row[country_field] is not None:
                            # Get media id's to assign to counts
                            media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                            counts.update({(media_id, self.recode_country(row[country_field])): row['n']})
                self.write_primary_row_heading(ws, region, r=r)
                region_countries = [(code, country) for code, country in self.countries if code in REGION_COUNTRY_MAP[region]]
                for i, row in enumerate(region_countries):
                    row_id, row_heading = row
                    ws.write(r+i, c, clean_title(row_heading), self.label)

                c += 1
                for col_id, col_heading in MEDIA_TYPES:
                    # values for this column
                    for i, row in enumerate(region_countries):
                        row_id, row_title = row

                        n = counts.get((col_id, row_id), 0)
                        ws.write(r+i, c, n, self.N)

                    c += 1
                # Position for next region
                c -= (len(MEDIA_TYPES) + 1)
                r += (len(region_countries) + 2)

            c += (len(MEDIA_TYPES) + 3)


    def write_raw_data_sheets(self, workbook):
        for name, model in sheet_models.items():
            ws = workbook.add_worksheet('Raw - %s sheets' % name)

            query = model.objects
            if self.country_list:
                query = query.filter(country__in=self.country_list)

            self.write_raw_data(ws, name, model, query, write_weights=True)

        for name, model in person_models.items():
            ws = workbook.add_worksheet('Raw - %s sources' % name)

            query = model.objects
            if self.country_list:
                query = query.filter(**{model.sheet_name() + '__country__in': self.country_list})\

            self.write_raw_data(ws, name, model, query)

        for name, model in journalist_models.items():
            ws = workbook.add_worksheet('Raw - %s journalists' % name)

            query = model.objects
            if self.country_list:
                query = query.filter(**{model.sheet_name() + '__country__in': self.country_list})\

            self.write_raw_data(ws, name, model, query)

    def write_raw_data(self, ws, name, model, query, write_weights=False):
        self.log.info("Writing raw data for %s" % model)

        # precompute the columns that are lookups
        lookups = {}
        for fld in model._meta.fields:
            if fld.choices:
                lookups[fld.attname] = dict(fld.choices)
            # TODO: handle foreign key, too

        # headers
        c = 0
        for fld in model._meta.fields:
            attr = fld.attname
            if attr in lookups:
                ws.write(0, c, fld.name + '_code')
                c += 1

            ws.write(0, c, fld.name)
            c += 1

            if attr == 'topic':
                ws.write(0, c, 'major topic')
                c += 1
                ws.write(0, c, 'women focus topic')
                c += 1

        # Add column for weights
        if write_weights:
            ws.write(0, c, "Weight")
            weights = Weights.objects.all()
            weights = {(w.country, w.media_type): w.weight for w in weights}

        country_regions = CountryRegion.objects.all()
        country_regions = {cr.id: cr.region for cr in country_regions}

        # values
        for r, obj in enumerate(query.all()):
            c = 0
            for fld in obj._meta.fields:
                attr = fld.attname
                if attr == 'country':
                    v = countries.alpha3(obj.country.code)

                elif attr == 'country_region_id':
                    v = country_regions[obj.country_region_id]

                else:
                    v = getattr(obj, attr)

                if isinstance(v, datetime.datetime):
                    v = v.replace(tzinfo=None)

                # raw value
                try:
                    basestring
                except NameError:
                    basestring = str
                if isinstance(v, basestring):
                    # if v is a URL and it contains unicode and it is
                    # very long, we get an encoding error from the warning
                    # message, so just force strings as strings
                    ws.write_string(r + 1, c, str(v))
                else:
                    ws.write(r + 1, c, v)
                c += 1

                # write the looked-up value
                actual_v = v
                if attr in lookups:
                    choices = lookups[attr]
                    if attr == 'country':
                        v = choices.get(obj.country.code, v)
                    else:
                        v = choices.get(v, v)
                    if v is not None:
                        v = str(v)
                    ws.write(r + 1, c, v)
                    c += 1

                if attr == 'topic':
                    # major topics
                    t = MAJOR_TOPICS[TOPIC_GROUPS[actual_v] - 1][1]
                    ws.write(r + 1, c, t)
                    c += 1

                    # women focus topic
                    t = FOCUS_TOPIC_ID_MAP.get(actual_v)
                    if t:
                        t = FOCUS_TOPICS[t - 1][1]
                    ws.write(r + 1, c, t)
                    c += 1

            if write_weights:
                # Write weight
                weight = weights[(obj.country, name)]
                # weight = [w.weight for w in weights if
                #             w.country == obj.country and
                #             w.media_type == name][0]

                ws.write(r + 1, c, weight)

    def recode_country(self, country):
        # some split countries must be "joined" at the global report level
        if self.report_type == 'global':
            return COUNTRY_RECODES.get(country, country)
        return country

    def dictfetchall(self, cursor):
        """
        Returns all rows from a cursor as a dict
        """
        desc = cursor.description
        return [
            OrderedDict(list(zip([col[0] for col in desc], row)))
            for row in cursor.fetchall()
        ]

    def apply_weights(self, rows, db_table, media_type):
        """
        param rows: Queryset to apply the weights to
        param db_table: name of relevant sheet table
        param: media_type: media type to weigh by
        """
        query = rows.extra(
                tables=['reports_weights'],
                where=[
                    'reports_weights.country = %s.country' % (db_table),
                    'reports_weights.media_type = \'%s\'' % (media_type),
                ]).annotate()

        raw_query, params = query.query.sql_with_params()

        if self.report_type == 'country':
            weights = 'SELECT count(1) AS "n",'
        else:
            weights = 'SELECT cast(SUM(reports_weights.weight) as float) AS "n",'

        raw_query = raw_query.replace('SELECT', weights)
        
        cursor = connection.cursor()
        cursor.execute(raw_query, params)
        return self.dictfetchall(cursor)


    def ws_01(self, ws):
        """
        Cols: Media Type
        Rows: Region
        """
        counts_list = []
        for media_types, models in SHEET_MEDIA_GROUPS:
            counts = Counter()
            for media_type, model in models.items():
                rows = model.objects\
                        .values('country_region__region')\
                        .filter(country_region__region__in=self.region_list)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for row in rows:
                    if row['region'] is not None:
                        # Get media and region id's to assign to counts
                        media_id = [media[0] for media in media_types if media[1] == media_type][0]
                        region_id = [region[0] for region in self.regions if region[1] == row['region']][0]
                        counts.update({(media_id, region_id): row['n']})
            counts_list.append(counts)

        self.tabulate(ws, counts_list[0], TM_MEDIA_TYPES, self.regions, row_perc=True)
        c = ws.dim_colmax + 2
        self.tabulate(ws, counts_list[1], DM_MEDIA_TYPES, self.regions, row_perc=True, c=c, write_row_headings=False)
        c = ws.dim_colmax + 2

        self.tabulate_historical(ws, '01', MEDIA_TYPES, self.regions, c=c)

    def ws_02(self, ws):
        """
        Cols: Media Type
        Rows: Region, Country
        """
        r = 6
        c = 2

        weights = {(w.country, w.media_type): w.weight for w in Weights.objects.all()}
        first = True
        historical_c = None

        for region_id, region in self.regions:
            counts_list = []
            for media_types, models in SHEET_MEDIA_GROUPS:

                counts = Counter()
                for media_type, model in models.items():
                    rows = model.objects\
                            .values('country')\
                            .filter(country__in=self.country_list)\
                            .annotate(n=Count('id'))

                    # rows = self.apply_distinct_weights(rows, model._meta.db_table, media_type)
                    for row in rows:
                        if row['country'] is not None:
                            weight = weights[(row['country'], media_type)]
                            # Get media id's to assign to counts
                            media_id = [media[0] for media in media_types if media[1] == media_type][0]
                            counts.update({(media_id, self.recode_country(row['country'])): row['n'] * weight})
                    for key, value in counts.items():
                        counts[key] = int(round(value))
                counts_list.append(counts)

            self.write_primary_row_heading(ws, region, r=r)
            region_countries = [(code, country) for code, country in self.countries if code in REGION_COUNTRY_MAP[region]]
            self.tabulate(ws, counts_list[0], TM_MEDIA_TYPES, region_countries, row_perc=True, write_col_headings=True, r=r)
            c = 7
            self.tabulate(ws, counts_list[1], DM_MEDIA_TYPES, region_countries, row_perc=True, write_col_headings=True, write_row_headings=False, r=r, c=c)

            if historical_c is None:
                historical_c = ws.dim_colmax + 2

            self.tabulate_historical(ws, '02', MEDIA_TYPES, region_countries, r=r, c=historical_c, write_year=first, write_col_headings=first)
            first = False

            r += (len(region_countries) + 2)

    def ws_03(self, ws):
        """
        Cols: Media type
        Rows: Region
        """
        # calculate total N for each media type for 2015,
        # then we'll compare it to 2010 and get a %age change

        # get the historical data for 2010
        counts = {}

        for media_type, model in sheet_models.items():
            rows = model.objects\
                    .values('country_region__region')\
                    .annotate(n=Count(get_sheet_model_name_field(media_type), distinct=True))\
                    .filter(country_region__region__in=self.region_list)\
                    .annotate(n=Count('id'))

            for row in rows:
                region = row['country_region__region']
                if region is not None:
                    # Get media and region id's to assign to counts
                    media_id, media = [m for m in MEDIA_TYPES if m[1] == media_type][0]
                    region_id, region = [r for r in self.regions if r[1] == region][0]

                    counts.update({(media_id, region_id): row['n']})

        self.tabulate(ws, counts, MEDIA_TYPES, self.regions, raw_values=True, write_col_totals=False, unweighted=True)
        self.tabulate_historical(ws, '03', MEDIA_TYPES, self.regions, values_N=True)

    def ws_04(self, ws):
        """
        Cols: Region, Media type
        Rows: Major Topic
        """
        counts_list = []
        for media_types, models in SHEET_MEDIA_GROUPS:
            secondary_counts = OrderedDict()
            for region_id, region in self.regions:
                counts = Counter()
                for media_type, model in models.items():
                    rows = model.objects\
                            .values('topic')\
                            .filter(country_region__region=region)\
                            .filter(country__in=self.country_list)\
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    for r in rows:
                        # Get media id's to assign to counts
                        media_id = [media[0] for media in media_types if media[1] == media_type][0]
                        major_topic = TOPIC_GROUPS[r['topic']]
                        counts.update({(media_id, major_topic): r['n']})
                if self.report_type == 'country':
                    # we are showing a single country data so use the contry name for the column name
                    secondary_counts[self.countries[0][1]] = counts
                else:
                    secondary_counts[region] = counts
            counts_list.append(secondary_counts)

        self.tabulate_secondary_cols(ws, counts_list[0], TM_MEDIA_TYPES, MAJOR_TOPICS, row_perc=False, show_N=True)
        c = ws.dim_colmax + 2
        self.tabulate_secondary_cols(ws, counts_list[1], DM_MEDIA_TYPES, MAJOR_TOPICS, row_perc=False, c=c, show_N=True)
        c = ws.dim_colmax + 2

        self.tabulate_historical(ws, '04', self.regions, MAJOR_TOPICS, c=c, r=7, skip_major_col_heading=True)

    def ws_05(self, ws, gen_csv=False):
        """
        Cols: Subject sex
        Rows: Major Topic
        """
        counts_list = []
        overall_column = ws.dim_colmax
        for media_types, models in PERSON_MEDIA_GROUPS:
            media_title = ', '.join(m[1] for m in media_types)
            secondary_counts = OrderedDict()

            for media_type, model in models.items():
                if not media_title in secondary_counts:
                    secondary_counts[media_title] = Counter()

                counts = secondary_counts[media_title]
                topic_field = '%s__topic' % model.sheet_name()

                rows = model.objects\
                    .values('sex', topic_field)\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)
                for r in rows:
                    counts.update({(r['sex'], TOPIC_GROUPS[r['topic']]): r['n']})

            counts_list.append(secondary_counts)
        if gen_csv:
            # Generate CSV
            generate_csv("presence_of_women_5", ["Topic", "Gender", "Medium", "Count"], counts_list, ws_05_csv)
        else:
            self.tabulate_secondary_cols(ws, counts_list[0], self.male_female, MAJOR_TOPICS, row_perc=True)
            c = ws.dim_colmax + 2
            self.tabulate_secondary_cols(ws, counts_list[1], self.male_female, MAJOR_TOPICS, row_perc=True, c=c, write_row_headings=False)
            c = ws.dim_colmax + 2

            self.tabulate_historical(ws, '05', self.male_female, MAJOR_TOPICS, c=c, r=7, skip_major_col_heading=True)
            overall_row = ws.dim_rowmax+2
            write_overall = True
            for media_type in counts_list:
                for medium in media_type:
                    counts = media_type[medium]
                    value = sum([counts[x] for x in counts if x[0] in self.female_ids])
                    total = sum(counts.values())
                    self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall)
                    write_overall= False
                    overall_column += 4

    def ws_06(self, ws, gen_csv=False):
        """
        Cols: Region, Subject sex: female only
        Rows: Major Topics
        """
        c = 1
        for media_types, models in PERSON_MEDIA_GROUPS:
            self.write_primary_row_heading(ws, ', '.join([m[1] for m in media_types]), c=c+1, r=4)
            secondary_counts = OrderedDict()

            for region_id, region in self.regions:
                counts = Counter()
                for media_type, model in models.items():
                    topic_field = '%s__topic' % model.sheet_name()
                    rows = model.objects\
                        .values('sex', topic_field)\
                        .filter(**{model.sheet_name() + '__country_region__region':region})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        counts.update({(r['sex'], TOPIC_GROUPS[r['topic']]): r['n']})
                secondary_counts[region] = counts
            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, MAJOR_TOPICS, row_perc=True, filter_cols=self.female, show_N=True, c=c, r=8)
            c = ws.dim_colmax + 2

        self.tabulate_historical(ws, '06', self.female, MAJOR_TOPICS, major_cols=self.regions, show_N_and_P=True, r=7)

    def ws_07(self, ws):
        """
        Cols: Media Type
        Rows: Subject Sex
        """
        counts = Counter()
        for media_type, model in person_models.items():
            rows = model.objects\
                    .values('sex')\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            for r in rows:
                # Get media id's to assign to counts
                media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                counts.update({(media_id, r['sex']): r['n']})

        self.tabulate(ws, counts, MEDIA_TYPES, self.male_female, row_perc=False)
        self.tabulate_historical(ws, '07', MEDIA_TYPES, self.male_female, write_row_headings=False)

    def ws_08(self, ws):
        """
        Cols: Subject Sex
        Rows: Scope
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            if 'scope' in [field_name.name for field_name in model.sheet_field().remote_field.model._meta.get_fields()]:
                scope = '%s__scope' % model.sheet_name()
                rows = model.objects\
                        .values('sex', scope)\
                        .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['scope']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, SCOPE, row_perc=True, filter_cols=self.female)
        self.tabulate_historical(ws, '08', self.female, SCOPE, write_row_headings=False)

    def ws_09(self, ws, gen_csv=False):
        """
        Cols: Subject Sex
        Rows: Topic
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            topic = '%s__topic' % model.sheet_name()
            rows = model.objects\
                    .values('sex', topic)\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            counts.update({(r['sex'], r['topic']): r['n'] for r in rows})
        if gen_csv:
            generate_csv("sex_of_news_subjects_9", ["Topic", "Gender", "Count"], counts, ws_09_csv)
        else:
            self.tabulate(ws, counts, self.male_female,  [y for x in TOPICS for y in x[1]], row_perc=True, filter_cols=self.female)
            self.tabulate_historical(ws, '09', self.female, [y for x in TOPICS for y in x[1]], write_row_headings=False)

    def ws_10(self, ws):
        """
        Cols: Space
        Rows: Minor Topics
        :: Newspaper Sheets only
        """
        # Calculate row values for column
        counts = Counter()
        for media_type, model in sheet_models.items():
            if media_type == 'Print':
                rows = model.objects\
                        .values('space', 'topic')\
                        .filter(country__in=self.country_list)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for r in rows:
                    counts.update({(r['space'], TOPIC_GROUPS[r['topic']]): r['n']})

        self.tabulate(ws, counts, SPACE, MAJOR_TOPICS, row_perc=False)
        self.tabulate_historical(ws, '10', SPACE, MAJOR_TOPICS)

    def ws_11(self, ws):
        """
        Cols: Equality Rights
        Rows: Major Topics
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        for media_type, model in tm_sheet_models.items():
            if 'equality_rights' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                    .values('equality_rights', 'topic')\
                    .filter(country__in=self.country_list)\
                    .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for r in rows:
                    counts.update({(r['equality_rights'], TOPIC_GROUPS[r['topic']]): r['n']})

        self.tabulate(ws, counts, YESNO, MAJOR_TOPICS, row_perc=True)
        self.tabulate_historical(ws, '11', [*YESNO], MAJOR_TOPICS, write_row_headings=False)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[0] == 'Y'])
        total = sum(counts.values())
        self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=True)

    def ws_12(self, ws):
        """
        Cols: Region, Equality Rights
        Rows: Major Topics
        """
        secondary_counts = OrderedDict()
        for region_id, region_name in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.items():
                # Some models has no equality rights field
                if 'equality_rights' in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects\
                        .values('equality_rights', 'topic')\
                        .filter(country_region__region=region_name)\
                        .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    for r in rows:
                        counts.update({(r['equality_rights'], TOPIC_GROUPS[r['topic']]): r['n']})
            secondary_counts[region_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, MAJOR_TOPICS, row_perc=True)
        c = ws.dim_colmax + 2
        self.tabulate_historical(ws, '12', [*YESNO], MAJOR_TOPICS, c=c, r=7, major_cols=self.regions)

    def ws_13(self, ws):
        """
        Cols: Journalist Sex, Equality Rights
        Rows: Topics
        """
        secondary_counts = OrderedDict()
        overall_column = ws.dim_colmax
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.items():
                if 'equality_rights' in [field_name.name for field_name in model.sheet_field().remote_field.model._meta.get_fields()]:
                    topic = '%s__topic' % model.sheet_name()
                    equality_rights = '%s__equality_rights' % model.sheet_name()
                    rows = model.objects\
                            .values(equality_rights, topic)\
                            .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                            .filter(sex=gender_id)\
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        counts.update({(r['equality_rights'], TOPIC_GROUPS[r['topic']]): r['n']})
            secondary_counts[gender] = counts      
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, MAJOR_TOPICS, row_perc=True)
        self.tabulate_historical(ws, '13', [*YESNO], MAJOR_TOPICS, write_row_headings=True, major_cols=self.male_female)        
        overall_row = ws.dim_rowmax + 2
        write_overall = True
        for gender in secondary_counts:
            counts = secondary_counts[gender]
            value = sum([counts[x] for x in counts if x[0] == 'Y'])
            total = sum(counts.values())
            self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall)
            overall_column+=3
            write_overall = False

    def ws_14(self, ws):
        """
        Cols: Sex
        Rows: Occupation
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            # some Person models don't have an occupation field
            if 'occupation' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', 'occupation')\
                        .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, OCCUPATION, row_perc=True, filter_cols=self.female)
        self.tabulate_historical(ws, '14', self.female, OCCUPATION, write_row_headings=False)

    def ws_15(self, ws, gen_csv=False):
        """
        Cols: Sex
        Rows: Function
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            # some Person models don't have a function field
            if 'function' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', 'function')\
                        .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['function']): r['n'] for r in rows})
        if gen_csv:
            generate_csv("function_of_news_subjects_15", ["Function", "Gender", "Count"], counts, ws_15_csv)
        else:
            self.tabulate(ws, counts, self.male_female, FUNCTION, row_perc=True, filter_cols=self.female)
            self.tabulate_historical(ws, '15', self.female, FUNCTION, write_row_headings=False)

    def ws_16(self, ws):
        """
        Cols: Function, Sex
        Rows: Occupation
        """
        secondary_counts = OrderedDict()
        for function_id, function in FUNCTION:
            counts = Counter()
            for media_type, model in tm_person_models.items():
                if 'function' and 'occupation' in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects\
                            .values('sex', 'occupation')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(function=function_id)\
                            .filter(sex__in=self.male_female_ids)\
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})
            secondary_counts[function] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, OCCUPATION, row_perc=False)
        self.tabulate_historical(ws, '16', self.male_female, OCCUPATION, major_cols=FUNCTION)

    def ws_17(self, ws):
        """
        Cols: Age, Sex of Subject
        Rows: Function
        """
        secondary_counts = OrderedDict()
        for age_id, age in AGES_PEOPLE_IN_THE_NEWS:
            counts = Counter()
            for media_type, model in tm_person_models.items():
                if 'function' and 'age' in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects\
                            .values('sex', 'function')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(age=age_id)\
                            .filter(sex__in=self.male_female_ids)\
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['sex'], r['function']): r['n'] for r in rows})
            secondary_counts[age] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, FUNCTION, row_perc=False)
        self.tabulate_historical(ws, '17', self.male_female, FUNCTION, major_cols=AGES)

    def ws_18(self, ws):
        """
        Cols: Sex
        Rows: Age
        :: Only for print
        """
        counts = Counter()
        rows = NewspaperPerson.objects\
                .values('sex', 'age')\
                .filter(newspaper_sheet__country__in=self.country_list)\
                .filter(sex__in=self.male_female_ids)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, NewspaperPerson.sheet_db_table(), 'Print')
        counts.update({(r['sex'], r['age']): r['n'] for r in rows})
        self.tabulate(ws, counts, self.male_female, AGES_PEOPLE_IN_THE_NEWS, row_perc=True)

        self.tabulate_historical(ws, '18', self.male_female, AGES, write_row_headings=False)

    def ws_19(self, ws):
        """
        Cols: Sex
        Rows: Age
        :: Only for broadcast
        """
        counts = Counter()
        broadcast = ['Television']
        for media_type, model in person_models.items():
             if media_type in broadcast:
                rows = model.objects\
                        .values('sex', 'age')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        self.tabulate_secondary_cols(ws, {'Television': counts}, self.male_female, AGES_PEOPLE_IN_THE_NEWS, row_perc=True)
        major_cols = [(3, 'Television')]
        self.tabulate_historical(ws, '19', self.male_female, AGES, major_cols=major_cols, write_row_headings=True)

    def ws_20(self, ws):
        """
        Cols: Function, Sex
        Rows: Occupation
        """
        secondary_counts = OrderedDict()

        for func_id, function in FUNCTION:
            counts = Counter()
            for media_type, model in tm_person_models.items():
                if 'function' and 'occupation' in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects\
                            .values('sex', 'occupation')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(function=func_id)\
                            .filter(sex__in=self.male_female_ids)\
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})
            secondary_counts[function] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, OCCUPATION, row_perc=False)
        self.tabulate_historical(ws, '20', self.male_female, OCCUPATION, major_cols=FUNCTION)

    def ws_21(self, ws):
        """
        Cols: Subject Sex
        Rows: Victim type
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            if 'victim_of' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', 'victim_of')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .exclude(victim_of=None)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['victim_of']): r['n'] for r in rows})
        self.tabulate(ws, counts, self.male_female, VICTIM_OF, row_perc=False, show_N=True)
        self.tabulate_historical(ws, '21', self.male_female, VICTIM_OF)

    def ws_23(self, ws):
        """
        Cols: Subject Sex
        Rows: Survivor type
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            if 'survivor_of' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', 'survivor_of')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .exclude(survivor_of=None)\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['survivor_of']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, SURVIVOR_OF, row_perc=False, show_N=True)
        self.tabulate_historical(ws, '23', self.male_female, SURVIVOR_OF)

    def ws_24(self, ws):
        """
        Cols: Subject Sex
        Rows: Family Role
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            if 'family_role' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', 'family_role')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['family_role']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, YESNO, row_perc=False)
        self.tabulate_historical(ws, '24', self.male_female, YESNO)

    def ws_25(self, ws):
        """
        Cols: Journalist Sex, Subject Sex
        Rows: Family Role
        """
        secondary_counts = OrderedDict()
        for sex_id, sex in self.male_female:
            counts = Counter()
            for media_type, model in tm_person_models.items():
                if 'family_role' in [field_name.name for field_name in model._meta.get_fields()]:
                    sheet_name = model.sheet_name()
                    journo_name = model._meta.get_field(model.sheet_name()).remote_field.model.journalist_field_name()
                    rows = model.objects\
                            .values('sex', 'family_role')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(**{sheet_name + '__' + journo_name + '__sex':sex_id})\
                            .filter(sex__in=self.male_female_ids)\
                            .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        rows = rows.filter(**{sheet_name + '__' + journo_name + '__role':REPORTERS})

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)
                    counts.update({(r['sex'], r['family_role']): r['n'] for r in rows})
            secondary_counts[sex] = counts

        secondary_counts['col_title_def'] = [
            'Sex of reporter',
            'Sex of news subject']

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, YESNO, row_perc=False)
        self.tabulate_historical(ws, '25', self.male_female, YESNO, major_cols=self.male_female, write_row_headings=False)

    def ws_26(self, ws):
        """
        Cols: Subject Sex
        Rows: Whether Quoted
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            if 'is_quoted' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', 'is_quoted')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['is_quoted']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, YESNO, row_perc=False)
        self.tabulate_historical(ws, '26', self.male_female, YESNO, write_row_headings=False)

    def ws_27(self, ws):
        """
        Cols: Subject Sex
        Rows: Photographed
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            if 'is_photograph' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', 'is_photograph')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['is_photograph']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, IS_PHOTOGRAPH, row_perc=False)
        self.tabulate_historical(ws, '27', self.male_female, IS_PHOTOGRAPH, write_row_headings=False)

    def ws_28(self, ws):
        """
        Cols: Medium, Journalist Sex
        Rows: Region
        :: Reporters + Presenters
        """
        overall_column = ws.dim_colmax
        if self.report_type == 'country':
            secondary_counts = OrderedDict()
            for media_type, model in tm_journalist_models.items():
                counts = Counter()
                country = model.sheet_name() + '__country'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    counts.update({(row['sex'], row['country']): row['n']})
                secondary_counts[media_type] = counts
            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)
        else:
            secondary_counts = OrderedDict()
            for media_type, model in tm_journalist_models.items():
                counts = Counter()
                region = model.sheet_name() + '__country_region__region'
                rows = model.objects\
                        .values('sex', region)\
                        .filter(**{region + '__in': self.all_region_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]

                    counts.update({(row['sex'], region_id): row['n']})
                secondary_counts[media_type] = counts
            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)
            self.tabulate_historical(ws, '28', self.male_female, self.regions, r=7)
        overall_row = ws.dim_rowmax + 2
        ws.write(overall_row, overall_column-1, "Overall", self.label)
        overall_column +=1
        for media_type in secondary_counts:
            counts = secondary_counts[media_type]
            value = sum([counts[x] for x in counts if x[0] in self.female_ids])
            total = sum(counts.values())
            self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=False)
            overall_column +=4

    def ws_28b(self, ws, gen_csv=False):
        """
        Cols: Media; Journo Type; Sex
        Rows: Country
        :: Newspaper, Television, Radio, Twitter, Internet by region and country
        """
        c = 1
        r = 8
        write_row_headings = True

        for media_type, model in journalist_models.items():
            if media_type in broadcast_journalist_models:
                reporter = [('Reporter', [2])]
            else:
                # Newspaper journos don't have roles
                reporter = [('Reporter', [])]

            col = c + (1 if write_row_headings else 0)
            merge_range = (len(reporter) * len(self.male_female) * 2) - 1

            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(media_type), self.col_heading)

            secondary_counts = OrderedDict()
            if self.report_type == 'country':
                for journo_type, role_ids in reporter:
                    counts = Counter()
                    country = model.sheet_name() + '__country'
                    rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        # Newspaper journos don't have roles
                        rows = rows.filter(role__in=role_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        counts.update({(row['sex'], row['country']): row['n']})

                    secondary_counts[journo_type] = counts
                if gen_csv:
                    generate_csv("reporters_by_region_medium_28b", ["Region", "Medium", "Gender", "Count"], secondary_counts, ws_28b_csv, medium=media_type, regions=dict(self.countries))
                else:
                    self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=r, write_row_headings=write_row_headings)

                    c += (len(reporter) * len(self.male_female) * 2) + (1 if write_row_headings else 0)
                    write_row_headings = False
            else:
                for journo_type, role_ids in reporter:
                    counts = Counter()
                    region = model.sheet_name() + '__country_region__region'

                    rows = model.objects\
                            .values('sex', region)\
                            .filter(**{region + '__in': self.all_region_list})\
                            .filter(sex__in=self.male_female_ids)\
                            .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        # Newspaper journos don't have roles
                        rows = rows.filter(role__in=role_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        region_id = [reg[0] for reg in self.all_regions if reg[1] == row["region"]][0]
                        counts.update({(row['sex'], region_id): row['n']})

                    secondary_counts[journo_type] = counts
                if gen_csv:
                    generate_csv("reporters_by_region_medium_28b", ["Region", "Medium", "Gender", "Count"], secondary_counts, ws_28b_csv, medium=media_type, regions=self.all_regions)    
                else:
                    self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True, c=c, r=r, write_row_headings=write_row_headings)
                    c += (len(reporter) * len(self.male_female) * 2) + (1 if write_row_headings else 0)
                    write_row_headings = False
    
    def ws_28c(self, ws, gen_csv=False):
        """
        Cols: Media; Journo Type; Sex
        Rows: Country
        :: Radio, Television by region and country
        """
        c = 1
        r = 8
        write_row_headings = True

        for media_type, model in broadcast_journalist_models.items():
            presenter = [('Presenter',[1, 3])]
            col = c + (1 if write_row_headings else 0)
            merge_range = (len(presenter) * len(self.male_female) * 2) - 1

            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(media_type), self.col_heading)

            secondary_counts = OrderedDict()
            if self.report_type == 'country':
                for journo_type, role_ids in presenter:
                    counts = Counter()
                    country = model.sheet_name() + '__country'
                    rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        # Newspaper journos don't have roles
                        rows = rows.filter(role__in=role_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        counts.update({(row['sex'], row['country']): row['n']})

                    secondary_counts[journo_type] = counts
                if gen_csv:
                    generate_csv("presenters_by_region_medium_28c", ["Region", "Medium", "Gender", "Count"], secondary_counts, ws_28c_csv, medium=media_type, regions=dict(self.countries))
                else:
                    self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=r, write_row_headings=write_row_headings)

                    c += (len(presenter) * len(self.male_female) * 2) + (1 if write_row_headings else 0)
                    write_row_headings = False
            else:
                for journo_type, role_ids in presenter:
                    counts = Counter()
                    region = model.sheet_name() + '__country_region__region'

                    rows = model.objects\
                            .values('sex', region)\
                            .filter(**{region + '__in': self.all_region_list})\
                            .filter(sex__in=self.male_female_ids)\
                            .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        # Newspaper journos don't have roles
                        rows = rows.filter(role__in=role_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        region_id = [reg[0] for reg in self.all_regions if reg[1] == row["region"]][0]
                        counts.update({(row['sex'], region_id): row['n']})

                    secondary_counts[journo_type] = counts
                if gen_csv:
                    generate_csv("presenters_by_region_medium_28c", ["Region", "Medium", "Gender", "Count"], secondary_counts, ws_28c_csv, medium=media_type, regions=self.all_regions)
                else:
                    self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True, c=c, r=r, write_row_headings=write_row_headings)
                    c += (len(presenter) * len(self.male_female) * 2) + (1 if write_row_headings else 0)
                    write_row_headings = False

    def ws_29(self, ws):
        """
        Cols: Regions, Journalist Sex
        Rows: Scope
        :: Reporters only
        """
        if self.report_type == 'country':
            secondary_counts = OrderedDict()
            for country_code, country_name in self.countries:
                counts = Counter()
                for media_type, model in tm_journalist_models.items():
                    sheet_name = model.sheet_name()
                    country = sheet_name + '__country'
                    scope =  sheet_name + '__scope'
                    if 'scope' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                        rows = model.objects\
                                .values('sex', scope)\
                                .filter(**{country + '__in': self.country_list})\
                                .filter(sex__in=self.male_female_ids)\
                                .annotate(n=Count('id'))
                        if media_type in REPORTER_MEDIA:
                            rows = rows.filter(role=REPORTERS)

                        rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                        for row in rows:
                            counts.update({(row['sex'], row['scope']): row['n']})
                secondary_counts[country_name] = counts
            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, SCOPE, row_perc=False, show_N=True)
        else:
            secondary_counts = OrderedDict()
            for region_id, region_name in self.regions:
                counts = Counter()
                for media_type, model in tm_journalist_models.items():
                    sheet_name = model.sheet_name()
                    region = sheet_name + '__country_region__region'
                    scope =  sheet_name + '__scope'
                    if 'scope' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                        rows = model.objects\
                                .values('sex', scope)\
                                .filter(**{region: region_name})\
                                .filter(sex__in=self.male_female_ids)\
                                .annotate(n=Count('id'))

                        if media_type in REPORTER_MEDIA:
                            rows = rows.filter(role=REPORTERS)

                        rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                        for row in rows:
                            counts.update({(row['sex'], row['scope']): row['n']})
                secondary_counts[region_name] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, SCOPE, row_perc=False, show_N=True)
        c = ws.dim_colmax + 2
        self.tabulate_historical(ws, '29', self.male_female, SCOPE, write_row_headings=True, c=c, major_cols=self.regions, show_N_and_P=True)

    def ws_30(self, ws, gen_csv=False):
        """
        Cols: Region, Sex of reporter
        Rows: Major Topics
        :: Reporters only
        """
        overall_column = ws.dim_colmax
        if self.report_type == 'country':
            secondary_counts = OrderedDict()
            for country_code, country_name in self.countries:
                counts = Counter()
                for media_type, model in tm_journalist_models.items():
                    sheet_name = model.sheet_name()
                    country = sheet_name + '__country'
                    topic =  sheet_name + '__topic'
                    if 'topic' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                        rows = model.objects\
                                .values('sex', topic)\
                                .filter(**{country + '__in': self.country_list})\
                                .filter(sex__in=self.male_female_ids)\
                                .annotate(n=Count('id'))

                        if media_type in REPORTER_MEDIA:
                            rows = rows.filter(role=REPORTERS)

                        rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                        for row in rows:
                            major_topic = TOPIC_GROUPS[row['topic']]
                            counts.update({(row['sex'], major_topic): row['n']})
                secondary_counts[country_name] = counts
            if not gen_csv:
                self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, MAJOR_TOPICS, row_perc=False, show_N=True)
        else:
            secondary_counts = OrderedDict()
            for region_id, region_name in self.regions:
                counts = Counter()
                for media_type, model in tm_journalist_models.items():
                    sheet_name = model.sheet_name()
                    region = sheet_name + '__country_region__region'
                    topic =  sheet_name + '__topic'
                    if 'topic' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                        rows = model.objects\
                                .values('sex', topic)\
                                .filter(**{region: region_name})\
                                .filter(sex__in=self.male_female_ids)\
                                .annotate(n=Count('id'))

                        if media_type in REPORTER_MEDIA:
                            rows = rows.filter(role=REPORTERS)

                        rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                        for row in rows:
                            major_topic = TOPIC_GROUPS[row['topic']]
                            counts.update({(row['sex'], major_topic): row['n']})
                secondary_counts[region_name] = counts
            if not gen_csv:
                self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, MAJOR_TOPICS, row_perc=False, show_N=True)
        if gen_csv:
            generate_csv("reporters_by_sex_topics_30", ["Region", "Topic", "Gender", "Count"], secondary_counts, ws_30_csv)    
        else:
            c = ws.dim_colmax + 2
            overall_row = ws.dim_rowmax + 2
            ws.write(overall_row, overall_column-1, "Overall", self.label)
            overall_column +=1
            for region in secondary_counts:
                counts = secondary_counts[region]
                value = sum([counts[x] for x in counts if x[0] in self.female_ids])
                total = sum(counts.values())
                self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=False)
                overall_column +=4
            self.tabulate_historical(ws, '30', self.male_female, MAJOR_TOPICS, write_row_headings=True, major_cols=self.regions, c=c, show_N_and_P=True)

    def ws_31(self, ws):
        """
        Cols: Sex of Reporter
        Rows: Minor Topics
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.items():
            sheet_name = model.sheet_name()
            topic =  sheet_name + '__topic'
            if 'topic' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', topic)\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(role=REPORTERS)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, [y for x in TOPICS for y in x[1]], row_perc=True, filter_cols=self.female)
        self.tabulate_historical(ws, '31', self.female, [y for x in TOPICS for y in x[1]], write_row_headings=False)

    def ws_32(self, ws):
        """
        Cols: Medium
        Rows: Topics
        :: Reporters only
        """
        secondary_counts = OrderedDict()
        journalist_models_items = [(media_type, model) for media_type, model in journalist_models.items() if media_type != "Twitter"]
        for media_type, model in journalist_models.items():
            counts = Counter()
            sheet_name = model.sheet_name()
            topic =  sheet_name + '__topic'
            if 'topic' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', topic)\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(role=REPORTERS)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    counts.update({(row['sex'], row['topic']): row['n']})
            secondary_counts[media_type] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, [y for x in TOPICS for y in x[1]], row_perc=False, show_N=True)
        c = ws.dim_colmax + 2
        self.tabulate_historical(ws, '32', self.male_female, [y for x in TOPICS for y in x[1]], write_row_headings=True, c=c, show_N_and_P=True, major_cols=TM_MEDIA_TYPES)

    def ws_34(self, ws):
        """
        Cols: Sex of reporter
        Rows: Sex of subject
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            sheet_name = model.sheet_name()
            journo_name = model._meta.get_field(model.sheet_name()).remote_field.model.journalist_field_name()
            journo_sex = sheet_name + '__' + journo_name + '__sex'
            rows = model.objects\
                    .extra(select={"subject_sex": model._meta.db_table + ".sex"})\
                    .values(journo_sex, 'subject_sex')\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .annotate(n=Count('id'))

            if media_type in REPORTER_MEDIA:
                rows = rows.filter(**{sheet_name + '__' + journo_name + '__role':REPORTERS})

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            counts.update({(r['sex'], r['subject_sex']): r['n'] for r in rows})
        counts['col_title_def'] = 'Sex of reporter'

        self.tabulate(ws, counts, self.male_female, GENDER, row_perc=True)
        self.tabulate_historical(ws, '34', self.female, GENDER, write_row_headings=False)

    def ws_35(self, ws):
        """
        Cols: Sex of reporter
        Rows: Age of reporter
        :: Only for television
        """
        secondary_counts = OrderedDict()

        counts = Counter()
        secondary_counts[TV_ROLE_ANNOUNCER[1]] = counts
        rows = TelevisionJournalist.objects\
                .values('sex', 'age')\
                .filter(television_sheet__country__in=self.country_list)\
                .filter(sex__in=self.male_female_ids)\
                .filter(role=TV_ROLE_ANNOUNCER[0])\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, TelevisionJournalist.sheet_db_table(), 'Television')
        counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        counts = Counter()
        secondary_counts[TV_ROLE_REPORTER[1]] = counts
        rows = TelevisionJournalist.objects\
                .values('sex', 'age')\
                .filter(television_sheet__country__in=self.country_list)\
                .filter(sex__in=self.male_female_ids)\
                .filter(role=TV_ROLE_REPORTER[0])\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, TelevisionJournalist.sheet_db_table(), 'Television')
        counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, AGES_PEOPLE_IN_THE_NEWS, row_perc=False, show_N=True)
        major_cols = [TV_ROLE_ANNOUNCER, TV_ROLE_REPORTER]
        self.tabulate_historical(ws, '35', self.female, AGES, major_cols=major_cols)

    def ws_36(self, ws):
        """
        Cols: Sex of Reporter
        Rows: Focus: about women
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.items():
            sheet_name = model.sheet_name()
            about_women =  sheet_name + '__about_women'
            if 'about_women' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                rows = model.objects\
                        .values('sex', about_women)\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(role=REPORTERS)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['about_women']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, YESNO, row_perc=False)
        self.tabulate_historical(ws, '36', self.male_female, YESNO, write_row_headings=False)

    def ws_38(self, ws, gen_csv=False):
        """
        Cols: Focus: about women
        Rows: Major Topics
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        for media_type, model in tm_sheet_models.items():
            if 'about_women' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('about_women', 'topic')\
                        .filter(country__in=self.country_list)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for r in rows:
                    counts.update({(r['about_women'], TOPIC_GROUPS[r['topic']]): r['n']})
        if gen_csv:
            generate_csv("stories_with_women_by_topics_38", ["Topic", "Answer", "Count"], counts, ws_38_csv)    
        else:
            self.tabulate(ws, counts, YESNO, MAJOR_TOPICS, row_perc=True)
            self.tabulate_historical(ws, '38', YESNO, MAJOR_TOPICS, write_row_headings=False)
            overall_row = ws.dim_rowmax + 2
            value = sum([counts[x] for x in counts if x[0] == 'Y'])
            total = sum(counts.values())
            self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=True)     

    def ws_39(self, ws):
        """
        Cols: Focus: about women
        Rows: Topics
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.items():
            if 'about_women' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('about_women', 'topic')\
                        .filter(country__in=self.country_list)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                counts.update({(r['about_women'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, YESNO, [y for x in TOPICS for y in x[1]], row_perc=True, filter_cols=self.yes)
        self.tabulate_historical(ws, '39', self.yes, [y for x in TOPICS for y in x[1]], write_row_headings=False)

    def ws_40(self, ws):
        """
        Cols: Region, Topics
        Rows: Focus: about women
        """
        secondary_counts = OrderedDict()
        for region_id, region in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.items():
                if 'about_women' in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects\
                            .values('topic', 'about_women')\
                            .filter(country_region__region=region)\
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    counts.update({(r['about_women'], r['topic']): r['n'] for r in rows})
            secondary_counts[region] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, [y for x in TOPICS for y in x[1]], row_perc=False, filter_cols=self.yes)
        self.tabulate_historical(ws, '40', self.yes, [y for x in TOPICS for y in x[1]], write_row_headings=False, major_cols=self.regions)

    def ws_41(self, ws, gen_csv=False):
        """
        Cols: Equality rights raised
        Rows: Topics
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        for media_type, model in tm_sheet_models.items():
            if 'equality_rights' in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values('equality_rights', 'topic')\
                        .filter(country__in=self.country_list)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
        if gen_csv:
            generate_csv("stories_with_gender_equality_41", ["Topic", "Answer", "Count"], counts, ws_41_csv)    
        else:
            self.tabulate(ws, counts, YESNO, [y for x in TOPICS for y in x[1]], row_perc=False, show_N=True)
            self.tabulate_historical(ws, '41', [*YESNO], [y for x in TOPICS for y in x[1]], write_row_headings=False, r=6, show_N_and_P=True)
            overall_row = ws.dim_rowmax + 2
            value = sum([counts[x] for x in counts if x[0] == 'Y'])
            total = sum(counts.values())
            ws.write(overall_row, overall_column-1, "Overall", self.label)
            self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_42(self, ws):
        """
        Cols: Region, Equality rights raised
        Rows: Topics
        """
        secondary_counts = OrderedDict()
        for region_id, region in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.items():
                if 'equality_rights' in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects\
                            .values('topic', 'equality_rights')\
                            .filter(country_region__region=region)\
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
            secondary_counts[region] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, [y for x in TOPICS for y in x[1]], row_perc=True)
        self.tabulate_historical(ws, '42', [*YESNO], [y for x in TOPICS for y in x[1]], write_row_headings=False, major_cols=self.regions)

    def ws_43(self, ws):
        """
        Cols: Sex of reporter, Equality rights raised
        Cols: Topics
        """
        secondary_counts = OrderedDict()
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.items():
                sheet_name = model.sheet_name()
                topic = sheet_name + '__topic'
                equality_rights =  sheet_name + '__equality_rights'
                if 'equality_rights' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                    rows = model.objects\
                            .values(topic, equality_rights)\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(sex=gender_id)\
                            .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        rows = rows.filter(role=REPORTERS)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
            secondary_counts[gender] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, [y for x in TOPICS for y in x[1]], row_perc=True)
        self.tabulate_historical(ws, '43', [*YESNO], [y for x in TOPICS for y in x[1]], write_row_headings=False, major_cols=self.male_female)

    def ws_44(self, ws):
        """
        Cols: Sex of reporter, Equality rights raised
        Rows: Region
        """
        secondary_counts = OrderedDict()
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.items():
                sheet_name = model.sheet_name()
                region = sheet_name + '__country_region__region'
                equality_rights =  sheet_name + '__equality_rights'
                if 'equality_rights' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                    rows = model.objects\
                            .values(equality_rights, region)\
                            .filter(sex=gender_id)\
                            .filter(**{region + '__in':self.region_list})\
                            .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        rows = rows.filter(role=REPORTERS)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        region_id = [id for id, name in self.regions if name == r['region']][0]
                        counts.update({(r['equality_rights'], region_id): r['n']})
            secondary_counts[gender] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.regions, row_perc=True)
        self.tabulate_historical(ws, '44', [*YESNO], self.regions, write_row_headings=False, major_cols=self.male_female)

    def ws_45(self, ws):
        """
        Cols: Sex of news subject
        Rows: Region
        :: Equality rights raised == Yes
        """
        counts = Counter()
        for media_type, model in tm_person_models.items():
            if 'equality_rights' in [field_name.name for field_name in model.sheet_field().remote_field.model._meta.get_fields()]:
                region = model.sheet_name() + '__country_region__region'
                equality_rights = model.sheet_name() + '__equality_rights'
                rows = model.objects\
                        .values('sex', region)\
                        .filter(**{region + '__in':self.region_list})\
                        .filter(**{equality_rights:'Y'})\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for r in rows:
                    region_id = [id for id, name in self.regions if name == r['region']][0]
                    counts.update({(r['sex'], region_id): r['n']})
        self.tabulate(ws, counts, self.male_female, self.regions, row_perc=True)
        self.tabulate_historical(ws, '45', self.male_female, self.regions, write_row_headings=False)

    def ws_46(self, ws):
        """
        Cols: Region, Stereotypes
        Rows: Major Topics
        """
        secondary_counts = OrderedDict()
        for _, region in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.items():
                if 'stereotypes' in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects \
                            .values('stereotypes', 'topic') \
                            .filter(country_region__region=region) \
                            .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    for row in rows:
                        major_topic = TOPIC_GROUPS[row['topic']]
                        counts.update({(row['stereotypes'], major_topic): row['n']})

            secondary_counts[region] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=True)
        self.tabulate_historical(ws, '46', AGREE_DISAGREE, MAJOR_TOPICS, write_row_headings=False, major_cols=self.regions)

    def ws_47(self, ws, gen_csv=False):
        """
        Cols: Stereotypes
        Rows: Major Topics
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                    .values('stereotypes', 'topic')\
                    .filter(country__in=self.country_list)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, media_type)

            for r in rows:
                counts.update({(r['stereotypes'], TOPIC_GROUPS[r['topic']]): r['n']})
        if gen_csv:
            generate_csv("stories_with_stereotypes_47", ["Topic", "Answer", "Count"], counts, ws_47_csv)    
        else:
            self.tabulate(ws, counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=True)
            self.tabulate_historical(ws, '47', AGREE_DISAGREE, MAJOR_TOPICS, write_row_headings=False)
            overall_row = ws.dim_rowmax + 2
            value = sum([counts[x] for x in counts if x[0] == 1])
            total = sum(counts.values())
            self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=True)

    def ws_48(self, ws, gen_csv=False):
        """
        Cols: Sex of reporter, Stereotypes
        Rows: Major Topics
        """
        secondary_counts = OrderedDict()
        overall_column = ws.dim_colmax
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.items():
                sheet_name = model.sheet_name()
                topic = sheet_name + '__topic'
                stereotypes =  sheet_name + '__stereotypes'
                if 'stereotypes' in [field_name.name for field_name in model._meta.get_field(sheet_name).remote_field.model._meta.get_fields()]:
                    rows = model.objects\
                            .values(stereotypes, topic)\
                            .filter(sex=gender_id)\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .annotate(n=Count('id'))

                    if media_type in REPORTER_MEDIA:
                        rows = rows.filter(role=REPORTERS)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        counts.update({(r['stereotypes'], TOPIC_GROUPS[r['topic']]): r['n']})
            secondary_counts[gender] = counts
            if gen_csv:
                generate_csv("stories_with_stereotypes_48", ["Topic", "Gender", "Answer", "Count"], counts, ws_48_csv, gender=gender_id)
        if not gen_csv:
            self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=True, show_N=True)
            self.tabulate_historical(ws, '48', AGREE_DISAGREE, MAJOR_TOPICS, write_row_headings=False, major_cols=self.male_female, show_N_and_P=True)
            overall_row = ws.dim_rowmax + 2
            # Female Overall
            counts = secondary_counts[self.male_female[0][1]]
            value = sum([counts[x] for x in counts if x[0] == 1])
            total = sum(counts.values())
            self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=True)
            # Male Overall
            counts = secondary_counts[self.male_female[1][1]]
            value = sum([counts[x] for x in counts if x[0] == 1])
            total = sum(counts.values())
            self.write_overall_value(ws, value, total, overall_column+5, overall_row, write_overall=True)     

    def ws_49(self, ws):
        """
        Cols: Major Topics
        Rows: Region
        :: Internet media type only
        """
        overall_column = ws.dim_colmax
        if self.report_type == 'country':
            counts = Counter()
            model = sheet_models.get('Internet')
            rows = model.objects\
                    .values('topic', 'country')\
                    .filter(country__in=self.country_list)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

            for row in rows:
                major_topic = TOPIC_GROUPS[row['topic']]
                counts.update({(major_topic, row['country']): row['n']})

            self.tabulate(ws, counts, MAJOR_TOPICS, self.countries, row_perc=True)
        else:
            counts = Counter()
            model = sheet_models.get('Internet')
            rows = model.objects\
                    .values('topic', 'country_region__region')\
                    .filter(country_region__region__in=self.region_list)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.regions if r[1] == row['region']][0]
                major_topic = TOPIC_GROUPS[row['topic']]
                counts.update({(major_topic, region_id): row['n']})

            self.tabulate(ws, counts, MAJOR_TOPICS, self.regions, row_perc=True)
            self.tabulate_historical(ws, '49', [*MAJOR_TOPICS], self.regions, write_row_headings=False)
        overall_row = ws.dim_rowmax + 2
        total = sum(counts.values())
        write_overall=True
        for topic, _ in MAJOR_TOPICS:
            value = sum([counts[x] for x in counts if x[0] == topic])
            self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall)
            write_overall=False
            overall_column+=1

    def ws_50(self, ws):
        """
        Cols: Major Topics
        Rows: YES NO
        :: Internet media type only
        :: Only stories shared on Twitter
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'shared_via_twitter')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))
        rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

        for row in rows:
            major_topic = TOPIC_GROUPS[row['topic']]
            counts.update({(major_topic, row['shared_via_twitter']): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, YESNO, show_N=True)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[1] == 'Y'])
        total = sum(counts.values())
        ws.write(overall_row, overall_column-1, "Overall Yes", self.label)
        self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_51(self, ws):
        """
        Cols: Major Topics
        Rows: YES NO
        :: Internet media type only
        :: Only stories shared on Facebook
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'shared_on_facebook')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

        for row in rows:
            major_topic = TOPIC_GROUPS[row['topic']]
            counts.update({(major_topic, row['shared_on_facebook']): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, YESNO, show_N=True)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[1] == 'Y'])
        total = sum(counts.values())
        ws.write(overall_row, overall_column-1, "Overall Yes", self.label)
        self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_52(self, ws):
        """
        Cols: Major Topics
        Rows: YES NO
        :: Internet media type only
        :: Only stories with reference to gener equality
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'equality_rights')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

        for row in rows:
            major_topic = TOPIC_GROUPS[row['topic']]
            counts.update({(major_topic, row['equality_rights']): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, YESNO, show_N=True)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[1] == 'Y'])
        total = sum(counts.values())
        ws.write(overall_row, overall_column-1, "Overall Yes", self.label)
        self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_53(self, ws):
        """
        Cols: Topic
        Rows: Country
        :: Internet media type only
        :: Female reporters only
        """
        filter_cols = [(id, value) for id, value in GENDER if id==1]
        secondary_counts = OrderedDict()
        model = sheet_models.get('Internet')

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            journo_sex_field = '%s__sex' % model.journalist_field_name()
            rows = model.objects\
                .values(journo_sex_field, 'country')\
                .filter(topic__in=topic_ids)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, 'Internet')
            counts.update({(r['sex'], self.recode_country(r['country'])): r['n'] for r in rows})
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.countries, row_perc=True, filter_cols=filter_cols)
        self.tabulate_historical(ws, '53', self.female, self.countries, major_cols=MAJOR_TOPICS)

    def ws_54(self, ws):
        """
        Cols: Major Topic, sex of subject
        Rows: Country
        :: Internet media type only
        """
        secondary_counts = OrderedDict()
        model = person_models.get('Internet')
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            country_field = '%s__country' % model.sheet_name()
            rows = model.objects\
                .values('sex', country_field)\
                .filter(**{model.sheet_name() + '__topic__in':topic_ids})\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')
            counts.update({(r['sex'], self.recode_country(r['country'])): r['n'] for r in rows})
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.countries, row_perc=True)
        self.tabulate_historical(ws, '54', [*GENDER], self.countries, major_cols=MAJOR_TOPICS)

    def ws_55(self, ws):
        """
        Cols: Occupation
        Rows: Gender
        :: Show male and female
        :: Internet and Twitter media types
        """
        secondary_counts = OrderedDict()

        for media_type, model in dm_person_models.items():
            counts = Counter()
            rows = model.objects\
                    .values('occupation', 'sex')\
                    .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                    .exclude(sex=None)\
                    .exclude(occupation=None)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)
            for d in rows:
                counts[d['sex'], d['occupation']] += d['n']
            
            secondary_counts[media_type] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, OCCUPATION, row_perc=True, show_N=True)

    def ws_56(self, ws):
        """
        Cols: Function
        Rows: Male Female
        :: Internet media and Twitter media types.
        """
        secondary_counts = OrderedDict()
        for media_type, model in dm_person_models.items():
            counts = Counter()
            rows = model.objects\
                    .values('function', 'sex')\
                    .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            for d in rows:
                counts[d['sex'], d['function']] += d['n']
            secondary_counts[media_type] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, FUNCTION, row_perc=True, show_N=True)

    def ws_57(self, ws):
        """
        Cols: Sex of subject
        Rows: Family role
        :: Internet media type only
        """

        counts = Counter()
        model = person_models.get('Internet')
        rows = model.objects\
                .values('sex', 'family_role')\
                .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        {counts.update({(row['sex'], row['family_role']): row['n']}) for row in rows}
        self.tabulate(ws, counts, GENDER, YESNO, show_N=True)

    def ws_58(self, ws):
        """
        Cols: Sex of subject
        Rows: is photographed
        :: Internet media type only
        """
        counts = Counter()
        model = person_models.get('Internet')
        
        rows = model.objects\
                .values('sex', 'is_photograph')\
                .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        for d in rows:
           counts[d['sex'], d['is_photograph']] += d['n']
        self.tabulate(ws, counts, GENDER, IS_PHOTOGRAPH, show_N=True)

    def ws_59(self, ws):
        """
        Cols: Sex of reporter
        Rows: Sex of subject
        :: Internet media only
        """
        counts = Counter()
        model = person_models.get('Internet')
        sheet_name = model.sheet_name()
        journo_name = model._meta.get_field(model.sheet_name()).remote_field.model.journalist_field_name()
        journo_sex = sheet_name + '__' + journo_name + '__sex'

        rows = model.objects\
                .extra(select={"subject_sex": model._meta.db_table + ".sex"})\
                .values(journo_sex, 'subject_sex')\
                .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        counts.update({(r['sex'], r['subject_sex']): r['n'] for r in rows})
        counts['col_title_def'] = 'Sex of reporter'

        self.tabulate(ws, counts, self.male_female, self.male_female, row_perc=False)
        self.tabulate_historical(ws, '59', self.male_female, self.male_female)

    def ws_60(self, ws):
        """
        Cols: Sex of subject
        Rows: age
        :: Internet media type only
        """
        counts = Counter()
        model = person_models.get('Internet')

        rows = model.objects\
                .values('sex', 'age')\
                .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        for d in rows:
           counts[d['sex'], d['age']] += d['n']

        self.tabulate(ws, counts, GENDER, AGES, show_N=True)

    def ws_61(self, ws):
        """
        Cols: Sex of subject
        Rows: is_quoted
        :: Internet media type only
        """
        counts = Counter()
        model = person_models.get('Internet')
        
        rows = model.objects\
                .values('sex', 'is_quoted')\
                .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        {counts.update({(row['sex'], row['is_quoted']): row['n']}) for row in rows}

        self.tabulate(ws, counts, GENDER, YESNO, show_N=True)

    def ws_62(self, ws):
        """
        Cols: Topic
        Rows: equality raised
        :: Internet media type only
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'equality_rights')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, "Internet")
        {counts.update({(TOPIC_GROUPS[row["topic"]], row["equality_rights"]): row['n']}) for row in rows}
        self.tabulate(ws, counts,  MAJOR_TOPICS, YESNO, show_N=True)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[1] == 'Y'])
        total = sum(counts.values())
        ws.write(overall_row, overall_column-1, "Overall Yes", self.label)
        self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_63(self, ws):
        """
        Cols: Topic
        Rows: stereotypes challenged
        :: Internet media type only
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        model = sheet_models.get('Internet')
        
        rows = model.objects\
                .values('topic', 'stereotypes')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, "Internet")

        {counts.update({(TOPIC_GROUPS[row["topic"]], row["stereotypes"]): row['n']}) for row in rows}

        self.tabulate(ws, counts,  MAJOR_TOPICS, AGREE_DISAGREE, show_N=True)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[1] == 1])
        total = sum(counts.values())
        ws.write(overall_row, overall_column-1, "Overall Agree", self.label)
        self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_64(self, ws):
        """
        Cols: Topic
        Rows: about women
        :: Internet media type only
        """
        counts = Counter()
        model = sheet_models.get('Internet')
        
        rows = model.objects\
                .values('topic', 'about_women')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, "Internet")
        {counts.update({(TOPIC_GROUPS[row["topic"]], row["about_women"]): row['n']}) for row in rows}

        self.tabulate(ws, counts, MAJOR_TOPICS, YESNO, show_N=True)

    def ws_65(self, ws):
        """
        Cols: Major Topic
        Rows: tweet or retweet
        :: Twitter media type only
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        model = sheet_models.get('Twitter')

        rows = model.objects\
                .values('topic', 'retweet')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, "Twitter")

        {counts.update({(TOPIC_GROUPS[row["topic"]], row["retweet"]): row['n']}) for row in rows}

        self.tabulate(ws, counts,  MAJOR_TOPICS, RETWEET, show_N=True)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[1] == 1])
        total = sum(counts.values())
        ws.write(overall_row, overall_column-1, "Overall Original Tweets", self.label)
        self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_66(self, ws):
        """
        Cols: Major Topic
        Rows: Country, sex of news subject
        :: Show all countries
        :: Twitter media type only
        """
        r = 6
        self.write_col_headings(ws, MAJOR_TOPICS)

        counts = Counter()
        model = person_models.get('Twitter')
        topic_field = '%s__topic' % model.sheet_name()
        for code, country in self.countries:
            rows = model.objects\
                    .values(topic_field, 'sex')\
                    .filter(**{model.sheet_name() + '__country':code})\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), "Twitter")

            counts = {(TOPIC_GROUPS[row['topic']], row['sex']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, MAJOR_TOPICS, GENDER, row_perc=True, write_col_headings=False, r=r)
            r += len(GENDER)

    def ws_67(self, ws):
        """
        Cols: Major Topic
        Rows: Country
        :: Only female journalists
        :: Show all countries
        :: Twitter media type only
        """
        counts = Counter()
        model = sheet_models.get('Twitter')
        rows = model.objects\
                .values('topic', 'country')\
                .filter(**{model.journalist_field_name() + '__sex':1})\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, "Twitter")
        {counts.update({(TOPIC_GROUPS[row['topic']], self.recode_country(row['country'])): row['n'] })for row in rows}
        self.tabulate(ws, counts, MAJOR_TOPICS, self.countries, row_perc=True)

    def ws_68(self, ws):
        """
        Cols: Major Topic
        Rows: Country, about women
        :: Show all countries
        :: Twitter media type only
        """
        r = 6
        self.write_col_headings(ws, MAJOR_TOPICS)

        counts = Counter()
        model = sheet_models.get('Twitter')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'about_women')\
                    .filter(country=code)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, "Twitter")

            {counts.update({(TOPIC_GROUPS[row['topic']], row['about_women']): row['n']}) for row in rows}
            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, MAJOR_TOPICS, YESNO, row_perc=False, write_col_headings=False, r=r)
            r += len(YESNO)

    def ws_68b(self, ws):
        """
        Cols: Topic
        Rows: Country, stereotypes
        :: Show all countries
        :: Twitter media type only
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        model = sheet_models.get('Twitter')
        rows = model.objects\
                .values('topic', 'stereotypes')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model._meta.db_table, "Twitter")
        for row in rows:
            counts.update({(TOPIC_GROUPS[row["topic"]], row["stereotypes"]): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, AGREE_DISAGREE, row_perc=True)
        overall_row = ws.dim_rowmax + 2
        value = sum([counts[x] for x in counts if x[1] == 1])
        total = sum(counts.values())
        self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=True)

    def ws_70(self, ws):
        ws.write(4, 0, 'See raw data sheets')

    def ws_71(self, ws):
        """
        Cols: Topic, Media type
        Rows: Country, Female news subjects
        Focus: women's overall presence
        """
        secondary_counts = OrderedDict()
        for topic_id, topic in FOCUS_TOPICS:
            actual_topic_ids = FOCUS_TOPIC_IDS[topic_id]
            counts = Counter()
            secondary_counts[topic] = counts

            for media_type, model in sheet_models.items():
                media_id = [m[0] for m in MEDIA_TYPES if m[1] ==media_type][0]
                person_name = model.person_field_name()

                rows = model.objects\
                    .values('country')\
                    .filter(**{person_name + '__sex': self.female[0][0]})\
                    .filter(topic__in=actual_topic_ids)\
                    .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)
                counts.update({(media_id, self.recode_country(r['country'])): r['n'] for r in rows})

        self.tabulate_secondary_cols(ws, secondary_counts, MEDIA_TYPES, self.countries, write_col_totals=False, raw_values=True)

    def ws_72(self, ws):
        """
        Cols: Focus Topic, Media
        Rows: Country
        Focus: female reporters
        """
        # TODO: these values should be %age total of media in country/region

        secondary_counts = OrderedDict()
        for topic_id, topic in FOCUS_TOPICS:
            actual_topic_ids = FOCUS_TOPIC_IDS[topic_id]
            counts = Counter()
            secondary_counts[topic] = counts

            for media_type, model in sheet_models.items():
                journo_name = model.journalist_field_name()
                media_id = [m[0] for m in MEDIA_TYPES if m[1] == media_type][0]

                rows = model.objects\
                    .values('country')\
                    .filter(**{journo_name + '__sex': self.female[0][0]})\
                    .filter(topic__in=actual_topic_ids)\
                    .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(**{journo_name + '__role':REPORTERS})

                rows = self.apply_weights(rows, model._meta.db_table, media_type)
                counts.update({(media_id, self.recode_country(r['country'])): r['n'] for r in rows})

        self.tabulate_secondary_cols(ws, secondary_counts, MEDIA_TYPES, self.countries, write_col_totals=False, raw_values=True)

    def ws_73(self, ws):
        """
        Cols: Sex of reporter
        Rows: Focus Topic
        Focus: Female news subject
        """
        focus_topic_ids = []
        for k, v in FOCUS_TOPIC_IDS.items():
            focus_topic_ids.extend(v)
        counts = Counter()
        for media_type, model in journalist_models.items():
            sheet_name = model.sheet_name()
            person_name = model.sheet_field().remote_field.model.person_field_name()
            topic_field = sheet_name + '__topic'
            rows = model.objects\
                        .values('sex', topic_field)\
                        .filter(**{sheet_name + '__country__in':self.country_list})\
                        .filter(**{sheet_name + '__'+ person_name + '__sex':self.female[0][0]})\
                        .filter(**{sheet_name + '__topic__in':focus_topic_ids})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

            if media_type in REPORTER_MEDIA:
                rows = rows.filter(role=REPORTERS)

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            for r in rows:
                focus_topic_id = [k for k, v in FOCUS_TOPIC_IDS.items() if r['topic'] in v][0]
                counts.update({(r['sex'], focus_topic_id): r['n']})

        self.tabulate(ws, counts, self.male_female, FOCUS_TOPICS, raw_values=True, write_col_totals=False)


    def ws_74(self, ws):
        """
        Cols: Focus Topic
        Rows: Country, About Women
        Focus: female reporters
        """
        c = 1
        for media_types, models in SHEET_MEDIA_GROUPS:
            self.write_primary_row_heading(ws, ', '.join([m[1] for m in media_types]), c=c+1, r=4)

            secondary_counts = OrderedDict()
            for topic_id, topic in FOCUS_TOPICS:
                counts = Counter()
                secondary_counts[topic] = counts
                actual_topic_ids = FOCUS_TOPIC_IDS[topic_id]

                for media_type, model in models.items():
                    rows = model.objects\
                        .values('country', 'about_women')\
                        .filter(country__in=self.country_list)\
                        .filter(topic__in=actual_topic_ids)\
                        .annotate(n=Count('id'))

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)
                    counts.update({(r['about_women'], self.recode_country(r['country'])): r['n'] for r in rows})

            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.countries, row_perc=True, c=c, r=8)
            c = ws.dim_colmax + 2

    def ws_75(self, ws):
        """
        Cols: Topic, Stereotypes
        Rows: Country
        """
        c = 1
        for media_types, models in SHEET_MEDIA_GROUPS:
            self.write_primary_row_heading(ws, ', '.join([m[1] for m in media_types]), c=c+1, r=4)

            secondary_counts = OrderedDict()
            for topic_id, topic in FOCUS_TOPICS:
                counts = Counter()
                secondary_counts[topic] = counts
                actual_topic_ids = FOCUS_TOPIC_IDS[topic_id]

                for media_type, model in models.items():
                    if 'stereotypes' in [field_name.name for field_name in model._meta.get_fields()]:
                        rows = model.objects\
                            .values('stereotypes', 'country')\
                            .filter(topic__in=actual_topic_ids)\
                            .annotate(n=Count('id'))

                        rows = self.apply_weights(rows, model._meta.db_table, media_type)
                        counts.update({(r['stereotypes'], self.recode_country(r['country'])): r['n'] for r in rows})

            self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, self.countries, row_perc=True, c=c, r=8)
            c = ws.dim_colmax + 2

    def ws_76(self, ws):
        """
        Cols: Topic, Reference to gender equality
        Rows: Country
        """
        c = 1
        for media_types, models in SHEET_MEDIA_GROUPS:
            self.write_primary_row_heading(ws, ', '.join([m[1] for m in media_types]), c=c+1, r=4)

            secondary_counts = OrderedDict()
            for topic_id, topic in FOCUS_TOPICS:
                counts = Counter()
                actual_topic_ids = FOCUS_TOPIC_IDS[topic_id]

                for media_type, model in models.items():
                    if 'equality_rights' in [field_name.name for field_name in model._meta.get_fields()]:
                        rows = model.objects\
                            .values('equality_rights', 'country')\
                            .filter(topic__in=actual_topic_ids)\
                            .annotate(n=Count('id'))

                        rows = self.apply_weights(rows, model._meta.db_table, media_type)
                        counts.update({(r['equality_rights'], self.recode_country(r['country'])): r['n'] for r in rows})

                    secondary_counts[topic] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.countries, row_perc=True, c=c, r=8)
            c = ws.dim_colmax + 2

    def ws_77(self, ws):
        """
        Cols: Topic, victim_of
        Rows: Country
        """
        c = 1
        for media_types, models in PERSON_MEDIA_GROUPS:
            self.write_primary_row_heading(ws, ', '.join([m[1] for m in media_types]), c=c+1, r=4)

            secondary_counts = OrderedDict()
            for topic_id, topic in FOCUS_TOPICS:
                counts = Counter()
                actual_topic_ids = FOCUS_TOPIC_IDS[topic_id]

                for media_type, model in models.items():
                    if 'victim_of' in [field_name.name for field_name in model._meta.get_fields()]:
                        country_field = '%s__country' % model.sheet_name()
                        rows = model.objects\
                            .values('victim_of', country_field)\
                            .filter(**{model.sheet_name() + '__topic__in':actual_topic_ids})\
                            .annotate(n=Count('id'))

                        rows = self.apply_weights(rows, model.sheet_db_table(), media_type)
                        counts.update({(r['victim_of'], self.recode_country(r['country'])): r['n'] for r in rows})

                    secondary_counts[topic] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, VICTIM_OF, self.countries, row_perc=True, c=c, r=8)
            c = ws.dim_colmax + 2

    def ws_78(self, ws):
        """
        Cols: Topic, survivor_of
        Rows: Country
        """
        c = 1
        for media_types, models in PERSON_MEDIA_GROUPS:
            self.write_primary_row_heading(ws, ', '.join([m[1] for m in media_types]), c=c+1, r=4)

            secondary_counts = OrderedDict()
            for topic_id, topic in FOCUS_TOPICS:
                counts = Counter()
                actual_topic_ids = FOCUS_TOPIC_IDS[topic_id]

                for media_type, model in models.items():
                    if 'survivor_of' in [field_name.name for field_name in model._meta.get_fields()]:
                        country_field = '%s__country' % model.sheet_name()
                        rows = model.objects\
                            .values('survivor_of', country_field)\
                            .filter(**{model.sheet_name() + '__topic__in':actual_topic_ids})\
                            .annotate(n=Count('id'))

                        rows = self.apply_weights(rows, model.sheet_db_table(), media_type)
                        counts.update({(r['survivor_of'], self.recode_country(r['country'])): r['n'] for r in rows})

                    secondary_counts[topic] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, SURVIVOR_OF, self.countries, row_perc=True, c=c, r=8)
            c = ws.dim_colmax + 2

    def ws_79(self, ws):
        """
        Cols: Major Topics, Sex of news subject
        Rows: Region
        :: Internet media type only
        """
        secondary_counts = OrderedDict()
        model = person_models.get('Internet')
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            region_field = '%s__country_region__region' % model.sheet_name()
            rows = model.objects\
                .values('sex', region_field)\
                .filter(**{model.sheet_name() + '__topic__in':topic_ids})\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['sex'], region_id): row['n']})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.all_regions, row_perc=True)

    def ws_80(self, ws):
        """
        Cols: Major Topics, Minor Topics, Shared on Twitter
        Rows: Region
        :: Internet media type only
        """
        model = sheet_models.get('Internet')
        c = 1
        r = 8
        write_row_headings = True

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            # Write primary column heading
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            col = c + (1 if write_row_headings else 0)
            merge_range = (len(topic_ids) * len(self.male_female) * 2) - 1
            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(major_topic_name), self.col_heading)

            secondary_counts = OrderedDict()

            for minor_topic in topic_ids:
                counts = Counter()
                rows = model.objects\
                    .values('shared_via_twitter', 'country_region__region')\
                    .filter(topic__in=topic_ids)\
                    .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

                for row in rows:
                    region_id = [region[0] for region in self.all_regions if region[1] == row['region']][0]
                    counts.update({(row['shared_via_twitter'], region_id): row['n']})

                minor_topic_name = [mt[1] for mt in [y for x in TOPICS for y in x[1]] if mt[0] == int(minor_topic)][0]
                secondary_counts[minor_topic_name] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.all_regions, c=c, r=r, write_row_headings=write_row_headings, show_N=True, row_perc=True)

            c += (len(topic_ids) * len(YESNO) * 2) + (1 if write_row_headings else 0)
            write_row_headings = False


    def ws_81(self, ws):
        """
        Cols: Major Topics, Minor Topics, Shared on Facebook
        Rows: Region
        :: Internet media type only
        """
        model = sheet_models.get('Internet')
        c = 1
        r = 8
        write_row_headings = True

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            # Write primary column heading
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            col = c + (1 if write_row_headings else 0)
            merge_range = (len(topic_ids) * len(self.male_female) * 2) - 1
            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(major_topic_name), self.col_heading)

            secondary_counts = OrderedDict()

            for minor_topic in topic_ids:
                counts = Counter()
                rows = model.objects\
                    .values('shared_on_facebook', 'country_region__region')\
                    .filter(topic__in=topic_ids)\
                    .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

                for row in rows:
                    region_id = [region[0] for region in self.all_regions if region[1] == row['region']][0]
                    counts.update({(row['shared_on_facebook'], region_id): row['n']})

                minor_topic_name = [mt[1] for mt in [y for x in TOPICS for y in x[1]] if mt[0] == int(minor_topic)][0]
                secondary_counts[minor_topic_name] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.all_regions, c=c, r=r, write_row_headings=write_row_headings, show_N=True, row_perc=True)

            c += (len(topic_ids) * len(YESNO) * 2) + (1 if write_row_headings else 0)
            write_row_headings = False


    def ws_82(self, ws):
        """
        Cols: Major Topics, Minor Topics, Equality Rights
        Rows: Region
        :: Internet media type only
        """
        model = sheet_models.get('Internet')
        c = 1
        r = 8
        write_row_headings = True

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            # Write primary column heading
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            col = c + (1 if write_row_headings else 0)
            merge_range = (len(topic_ids) * len(self.male_female) * 2) - 1
            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(major_topic_name), self.col_heading)

            secondary_counts = OrderedDict()

            for minor_topic in topic_ids:
                counts = Counter()
                rows = model.objects\
                    .values('equality_rights', 'country_region__region')\
                    .filter(topic__in=topic_ids)\
                    .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

                for row in rows:
                    region_id = [region[0] for region in self.all_regions if region[1] == row['region']][0]
                    counts.update({(row['equality_rights'], region_id): row['n']})

                minor_topic_name = [mt[1] for mt in [y for x in TOPICS for y in x[1]] if mt[0] == int(minor_topic)][0]
                secondary_counts[minor_topic_name] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.all_regions, c=c, r=r, write_row_headings=write_row_headings, show_N=True, row_perc=True)

            c += (len(topic_ids) * len(YESNO) * 2) + (1 if write_row_headings else 0)
            write_row_headings = False


    def ws_83(self, ws, gen_csv=False):
        """
        Cols: Major Topics, Reporters by sex
        Rows: Region
        :: Internet media type only
        """
        secondary_counts = OrderedDict()
        model = journalist_models.get('Internet')

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            region_field = '%s__country_region__region' % model.sheet_name()
            rows = model.objects\
                .values('sex', region_field)\
                .filter(**{model.sheet_name() + '__topic__in':topic_ids})\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['sex'], region_id): row['n']})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts
        
        if gen_csv:
            generate_csv("stories_with_stereotypes_83", ["Topic", "Region", "Gender", "Count"], secondary_counts, ws_83_csv, regions=self.all_regions)
        else:
            self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.all_regions, row_perc=True)

    def ws_84(self, ws):
        """
        Cols: Occupation
        Rows: Region
        :: Internet media type only
        :: Female news subjects only
        """
        model = person_models.get('Internet')

        counts = Counter()
        region_field = '%s__country_region__region' % model.sheet_name()
        rows = model.objects\
            .values('occupation', region_field)\
            .filter(sex__in=self.female_ids)\
            .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

        for row in rows:
            region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
            counts.update({(row['occupation'], region_id): row['n']})

        self.tabulate(ws, counts, OCCUPATION, self.all_regions, row_perc=True, show_N=True)

    def ws_85(self, ws, gen_csv=False):
        """
        Cols: Function
        Rows: Region
        :: Internet media type only
        """
        model = person_models.get('Internet')

        counts = Counter()
        region_field = '%s__country_region__region' % model.sheet_name()
        rows = model.objects\
            .values('function', region_field)\
            .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

        for row in rows:
            region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
            counts.update({(row['function'], region_id): row['n']})
        if gen_csv:
            generate_csv("function_of_subjects_85", ["Region", "Function", "Count"], counts, ws_85_csv, regions=self.all_regions)
        else:
            self.tabulate(ws, counts, FUNCTION, self.all_regions, row_perc=True, show_N=True)

    def ws_86(self, ws):
        """
        Cols: Sex of subject, Identified by family status
        Rows: Region
        :: Internet media type only
        """
        model = person_models.get('Internet')
        secondary_counts = OrderedDict()
        for gender_id, gender in self.male_female:
            counts = Counter()
            region_field = '%s__country_region__region' % model.sheet_name()
            rows = model.objects\
                .values('family_role', region_field)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['family_role'], region_id): row['n']})
            secondary_counts[gender] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.all_regions, row_perc=True, show_N=True)

    def ws_87(self, ws):
        """
        Cols: Sex of subject, Photo or image present
        Rows: Region
        :: Internet media type only
        """
        model = person_models.get('Internet')
        secondary_counts = OrderedDict()

        for gender_id, gender in self.male_female:
            counts = Counter()
            region_field = '%s__country_region__region' % model.sheet_name()
            rows = model.objects\
                .values('is_photograph', region_field)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['is_photograph'], region_id): row['n']})
            secondary_counts[gender] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, IS_PHOTOGRAPH, self.all_regions, row_perc=True, show_N=True)

    def ws_88(self, ws):
        """
        Cols: Sex of reporter, Sex of subject
        Rows: Region
        :: Internet media type only
        """
        model = journalist_models.get('Internet')
        secondary_counts = OrderedDict()

        for gender_id, gender in self.male_female:
            counts = Counter()
            region_field = '%s__country_region__region' % model.sheet_name()

            rows = model.objects\
                .values('internetnews_sheet__internetnewsperson__sex', region_field)\
                .filter(sex=gender_id)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['sex'], region_id): row['n']})

            counts['col_title_def'] = 'Sex of news subject'
            secondary_counts[gender] = counts

        secondary_counts['col_title_def'] = [
            'Sex of reporter',
            'Sex of news subject']

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)

    def ws_89(self, ws):
        """
        Cols: Sex of subject, Age of news subject
        Rows: Region
        :: Internet media type only
        """
        model = person_models.get('Internet')
        secondary_counts = OrderedDict()

        for gender_id, gender in self.male_female:
            counts = Counter()
            region_field = '%s__country_region__region' % model.sheet_name()
            rows = model.objects\
                .values('age', region_field)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['age'], region_id): row['n']})
            secondary_counts[gender] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, AGES, self.all_regions, row_perc=True, show_N=True)

    def ws_90(self, ws):
        """
        Cols: Sex of subject, Whether quoted
        Rows: Region
        :: Internet media type only
        """
        model = person_models.get('Internet')
        secondary_counts = OrderedDict()

        for gender_id, gender in self.male_female:
            counts = Counter()
            region_field = '%s__country_region__region' % model.sheet_name()
            rows = model.objects\
                .values('is_quoted', region_field)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['is_quoted'], region_id): row['n']})
            secondary_counts[gender] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.all_regions, row_perc=True, show_N=True)

    def ws_91(self, ws):
        """
        Cols: Major Topic
        Rows: Region, equality raised
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, MAJOR_TOPICS)

        model = sheet_models.get('Internet')

        for region_id, region in self.all_regions:
            counts = Counter()
            rows = model.objects\
                    .values('topic', 'equality_rights')\
                    .filter(country_region__region=region)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, "Internet")
            for row in rows:
                major_topic = TOPIC_GROUPS[row['topic']]
                counts.update({(major_topic, row['equality_rights']): row['n']})

            self.write_primary_row_heading(ws, region, r=r)
            self.tabulate(ws, counts, MAJOR_TOPICS, YESNO, row_perc=True, write_col_headings=False, r=r)
            r += len(YESNO)

    def ws_92(self, ws, gen_csv=False):
        """
        Cols: Major Topic
        Rows: Region, stereotypes
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, MAJOR_TOPICS)

        model = sheet_models.get('Internet')

        for region_id, region in self.all_regions:
            counts = Counter()
            rows = model.objects\
                    .values('topic', 'stereotypes')\
                    .filter(country_region__region=region)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, "Internet")
            for row in rows:
                major_topic = TOPIC_GROUPS[row['topic']]
                counts.update({(major_topic, row['stereotypes']): row['n']})
            if not gen_csv:
                self.write_primary_row_heading(ws, region, r=r)
                self.tabulate(ws, counts, MAJOR_TOPICS, AGREE_DISAGREE, row_perc=True, write_col_headings=False, r=r)
                r += len(AGREE_DISAGREE)
            else:
                generate_csv("stereotypes_challenged_92", ["Region", "Topic", "Answer", "Count"], counts, ws_92_csv, region=region)

    def ws_93(self, ws):
        """
        Cols: Major Topic
        Rows: Region, about women
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, MAJOR_TOPICS)

        model = sheet_models.get('Internet')

        for region_id, region in self.all_regions:
            counts = Counter()
            rows = model.objects\
                    .values('topic', 'about_women')\
                    .filter(country_region__region=region)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, "Internet")
            for row in rows:
                major_topic = TOPIC_GROUPS[row['topic']]
                counts.update({(major_topic, row['about_women']): row['n']})

            self.write_primary_row_heading(ws, region, r=r)
            self.tabulate(ws, counts, MAJOR_TOPICS, YESNO, row_perc=True, write_col_headings=False, r=r)
            r += len(YESNO)


    def ws_94(self, ws):
        """
        Cols: Major Topics, Original tweet or retweet
        Rows: Region
        :: Twitter media type only
        """
        secondary_counts = OrderedDict()
        model = sheet_models.get('Twitter')

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            rows = model.objects\
                .values('retweet', 'country_region__region')\
                .filter(topic__in=topic_ids)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, 'Twitter')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['retweet'], region_id): row['n']})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, RETWEET, self.all_regions, row_perc=True)


    def ws_95(self, ws):
        """
        Cols: Major Topics, Female reporters
        Rows: Region
        :: Twitter media type only
        """
        model = journalist_models.get('Twitter')
        c = 1
        r = 8
        write_row_headings = True

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]

            # Write primary column heading
            col = c + (1 if write_row_headings else 0)
            merge_range = (len(topic_ids) * len(self.male_female) * 2) - 1
            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(major_topic_name), self.col_heading)

            secondary_counts = OrderedDict()
            for minor_topic in topic_ids:
                counts = Counter()
                region_field = '%s__country_region__region' % model.sheet_name()

                rows = model.objects\
                    .values('sex', region_field)\
                    .filter(**{model.sheet_name() + '__topic__in':topic_ids})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), 'Twitter')

                for row in rows:
                    region_id = [region[0] for region in self.all_regions if region[1] == row['region']][0]
                    counts.update({(row['sex'], region_id): row['n']})

                minor_topic_name = [mt[1] for mt in [y for x in TOPICS for y in x[1]] if mt[0] == int(minor_topic)][0]
                secondary_counts[minor_topic_name] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, c=c, r=r, write_row_headings=write_row_headings, show_N=True, row_perc=True)

            c += (len(topic_ids) * len(GENDER)) + (1 if write_row_headings else 0)
            write_row_headings = False


    def ws_96(self, ws):
        """
        Cols: Major Topics, Women's centrality
        Rows: Region
        :: Twitter media type only
        """
        secondary_counts = OrderedDict()
        model = sheet_models.get('Twitter')

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            rows = model.objects\
                .values('about_women', 'country_region__region')\
                .filter(topic__in=topic_ids)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, 'Twitter')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['about_women'], region_id): row['n']})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.all_regions, row_perc=True)


    def ws_97(self, ws):
        """
        Cols: Major Topics, Stereotypes
        Rows: Region
        :: Twitter media type only
        """
        secondary_counts = OrderedDict()
        model = sheet_models.get('Twitter')

        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            rows = model.objects\
                .values('stereotypes', 'country_region__region')\
                .filter(topic__in=topic_ids)\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, 'Twitter')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row['region']][0]
                counts.update({(row['stereotypes'], region_id): row['n']})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, self.all_regions, row_perc=True)

    def ws_98(self, ws):
        return
    
    def ws_100(self, ws):
        """
        Cols: Medium 
        Rows: Major topic
        """
        secondary_counts = OrderedDict()
        overall_column = grand_total_column = ws.dim_colmax
        for _, models in SHEET_MEDIA_GROUPS:
            for media_type, model in models.items():
                counts = Counter()
                rows = model.objects\
                        .values('covid19', 'topic') \
                        .filter(country__in=self.country_list) \
                        .annotate(n=Count('id'))
                        
                rows = self.apply_weights(rows, model._meta.db_table, media_type)
            
                for r in rows:
                    covid19 = 'Y' if r['covid19'] == 1 else 'N'
                    counts.update({(covid19, TOPIC_GROUPS[r['topic']]): r['n']})
                secondary_counts[media_type] = counts
    
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, MAJOR_TOPICS, row_perc=True)
        overall_row = ws.dim_rowmax + 2
        grand_total_yes_no = 0
        grand_total_yes = 0
        write_overall=True
        for medium in secondary_counts:
            counts = secondary_counts[medium]
            total = sum(counts.values())
            grand_total_yes_no += total
            value = sum([counts[x] for x in counts if x[0] == 'Y'])
            grand_total_yes += value

            self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall, overall_label="OVERALL BY MEDIUM")

            overall_column+=3
            write_overall= False     
        self.write_overall_value(ws, grand_total_yes, grand_total_yes_no, grand_total_column, overall_row+3, write_overall=True, overall_label="GRAND TOTAL")

    def ws_101(self, ws):
        """
        Cols: Reporters by sex
        Rows: Major topic, covid stories only
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        for media_type, model in sheet_models.items():
            rows = model.objects \
                .values("topic", model.journalist_field_name() + "__sex") \
                .filter(covid19=1,
                        **{model.journalist_field_name() + "__sex__in": self.male_female_ids},
                        country__in=self.country_list) \
                .annotate(n=Count("id"))

            rows = self.apply_weights(rows, model._meta.db_table, media_type)

            for r in rows:
                counts.update({(r["sex"], TOPIC_GROUPS[r["topic"]]): r["n"]})

        self.tabulate(ws, counts, GENDER, MAJOR_TOPICS, row_perc=True, show_N=True)
        overall_row = ws.dim_rowmax + 2
        total = sum(counts.values())
        value = sum([counts[x] for x in counts if x[0] in self.female_ids])
        ws.write(overall_row, overall_column-1, "Overall Female", self.label)
        self.write_overall_value(ws, value, total, overall_column+1, overall_row, write_overall=False)

    def ws_102(self, ws):
        """
        Cols: Gender stereotypes
        Rows: Major topic, covid stories only
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        for media_type, model in sheet_models.items():
            rows = (
                model.objects.values("stereotypes", "topic")
                .filter(covid19=1, country__in=self.country_list)
                .annotate(n=Count("id"))
            )

            rows = self.apply_weights(rows, model._meta.db_table, media_type)

            for r in rows:
                counts.update({(r["stereotypes"], TOPIC_GROUPS[r["topic"]]): r["n"]})

        self.tabulate(ws, counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=True)
        overall_row = ws.dim_rowmax + 2
        total = sum(counts.values())
        value = sum([counts[x] for x in counts if x[0] == 1])
        self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=True, overall_label="Overall Agree")
    
    def ws_103(self, ws):
        """
        Cols: Gender inequalities
        Rows: Major topic, covid stories only
        """
        counts = Counter()
        overall_column = ws.dim_colmax
        for media_type, model in sheet_models.items():
            if "equality_rights" in [field_name.name for field_name in model._meta.get_fields()]:
                rows = model.objects\
                        .values("equality_rights", "topic") \
                        .filter(covid19=1, country__in=self.country_list) \
                        .annotate(n=Count("id"))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for r in rows:
                    counts.update({(r["equality_rights"], TOPIC_GROUPS[r["topic"]]): r["n"]})

        self.tabulate(ws, counts, YESNO, MAJOR_TOPICS, row_perc=True) 
        overall_row = ws.dim_rowmax + 2
        total = sum(counts.values())
        value = sum([counts[x] for x in counts if x[0] == 'Y'])
        self.write_overall_value(ws, value, total, overall_column, overall_row, write_overall=True, overall_label="Overall Yes")  

    def ws_104(self, ws):
        """
        Cols: Function in story
        Rows: Major topic, covid stories only, Sex of source
        """
        r = 6
        c = 2
        for _, col_heading in FUNCTION:
            ws.merge_range(r-2, c, r-2, c+1, clean_title(col_heading), self.col_heading)
            ws.write(r - 1, c, "%")
            ws.write(r - 1, c + 1, "N")
            c += 2
            
        gender_ids = [x[0] for x in GENDER]
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            for media_type, model in person_models.items():
                # some Person models don't have a function field
                if "function" in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects \
                            .values("sex", "function") \
                            .filter(**{model.sheet_name() + "__covid19": 1}) \
                            .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                            .filter(**{model.sheet_name() + "__topic__in": topic_ids}) \
                            .filter(sex__in=gender_ids) \
                            .annotate(n=Count("id"))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r["function"], r["sex"]): r["n"] for r in rows})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            self.write_primary_row_heading(ws, major_topic_name, r=r)
            self.tabulate(ws, counts, FUNCTION, GENDER, write_col_headings=False, write_col_totals=False, r=r, show_N=True)
            r += len(GENDER)    

    def ws_105(self, ws):
        """
        Cols: Survivors
        Rows: Major topic, covid stories only, Sex of source
        """
        r = 6
        c = 2
        for _, col_heading in SURVIVOR_OF:
            ws.merge_range(r-2, c, r-2, c+1, clean_title(col_heading), self.col_heading)
            ws.write(r - 1, c, "%")
            ws.write(r - 1, c + 1, "N")
            c += 2
            
        gender_ids = [x[0] for x in GENDER]
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            for media_type, model in person_models.items():
                if "survivor_of" in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects \
                            .values("sex", "survivor_of") \
                            .filter(**{model.sheet_name() + "__covid19": 1}) \
                            .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                            .exclude(survivor_of=None) \
                            .filter(**{model.sheet_name() + "__topic__in": topic_ids}) \
                            .filter(sex__in=gender_ids) \
                            .annotate(n=Count("id"))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r["survivor_of"], r["sex"]): r["n"] for r in rows})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            self.write_primary_row_heading(ws, major_topic_name, r=r)
            self.tabulate(ws, counts, SURVIVOR_OF, GENDER, write_col_headings=False, write_col_totals=False, r=r, show_N=True)
            r += len(GENDER)

    def ws_106(self, ws):
        """
        Cols: Occupation
        Rows: Major topic, covid stories only, Sex of source
        """
        r = 6
        c = 2
        for _, col_heading in OCCUPATION:
            ws.merge_range(r-2, c, r-2, c+1, clean_title(col_heading), self.col_heading)
            ws.write(r - 1, c, "%")
            ws.write(r - 1, c + 1, "N")
            c += 2
            
        gender_ids = [x[0] for x in GENDER]
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            for media_type, model in person_models.items():
                if "occupation" in [field_name.name for field_name in model._meta.get_fields()]:
                    rows = model.objects \
                            .values("sex", "occupation") \
                            .filter(**{model.sheet_name() + "__covid19": 1}) \
                            .filter(**{model.sheet_name() + "__country__in": self.country_list}) \
                            .filter(**{model.sheet_name() + "__topic__in": topic_ids}) \
                            .filter(sex__in=gender_ids) \
                            .annotate(n=Count("id"))

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r["occupation"], r["sex"]): r["n"] for r in rows})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            self.write_primary_row_heading(ws, major_topic_name, r=r)
            self.tabulate(ws, counts, OCCUPATION, GENDER, write_col_headings=False, write_col_totals=False, r=r, show_N=True)
            r += len(GENDER)

    def ws_107(self, ws):
        """
        Cols: Medium 
        Rows: SQ 1,2,3, Major topic
        """
        r = 6
        c = 2
        for _, col_heading in MEDIA_TYPES:
            ws.merge_range(r-2, c, r-2, c+1, clean_title(col_heading), self.sec_col_heading)
            ws.write(r - 1, c, "Yes", self.col_heading)
            ws.write(r - 1, c + 1, "No", self.col_heading)
            c += 2
        
        secondary_counts = OrderedDict()
        for sq_field, sq in SPECIAL_QUESTIONS.items():
            for media_type, model in person_models.items():
                counts = Counter()
                sheet_name = model.sheet_name()
                rows = model.objects \
                        .values(sq_field, f"{sheet_name}__topic") \
                        .filter(**{f"{sheet_name}__country__in": self.country_list}) \
                        .exclude(**{sq_field: ""}) \
                        .annotate(n=Count("id"))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    counts.update({(row[sq_field], TOPIC_GROUPS[row['topic']]): row['n']})

                secondary_counts[media_type] = counts
            self.write_primary_row_heading(ws, sq, r=r)
            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, MAJOR_TOPICS, row_perc=False, write_primary_col_headins=False, write_col_headings=False, write_col_totals=False, r=r, raw_values=True)
            r += len(MAJOR_TOPICS)

    def ws_108(self, ws):
        """
        Cols: People in the news, by sex 
        Rows: SQ 1,2,3, Major topic
        """
        r = 6
        c = 2
        # Write definitions of column heading titles
        ws.write(r-1, c-1, "Sex of source", self.col_heading_def)
        for _, sec_col_heading in YESNO:
            ws.merge_range(r-2, c, r-2, c+len(GENDER)-1, clean_title(sec_col_heading), self.sec_col_heading)
            for _, col_heading in GENDER:
                ws.write(r-1, c, clean_title(col_heading), self.col_heading)
                c += 1


        secondary_counts = OrderedDict()
        for sq_field, sq in SPECIAL_QUESTIONS.items():
            for yes_no, _ in YESNO:
                counts = Counter()
                for media_type, model in person_models.items():
                    sheet_name = model.sheet_name()
                    rows = model.objects \
                            .values(sq_field, "sex", f"{sheet_name}__topic") \
                            .filter(**{f"{sheet_name}__country__in": self.country_list}) \
                            .exclude(**{sq_field: ""}) \
                            .filter(**{sq_field: yes_no}) \
                            .annotate(n=Count("id"))

                    rows= self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        counts.update({(row["sex"], TOPIC_GROUPS[row['topic']]): row['n']})

                secondary_counts[yes_no] = counts

            self.write_primary_row_heading(ws, sq, r=r)
            self.tabulate_secondary_cols(ws, secondary_counts, GENDER, MAJOR_TOPICS, row_perc=False, write_primary_col_headins=False, write_col_headings=False, write_col_totals=False, r=r, raw_values=True)
            r += len(MAJOR_TOPICS)

    def ws_109(self, ws):
        """
        Cols: Reporters by sex
        Rows: SQ 1,2,3, Major topic
        """
        r = 6
        c = 2
        # Write definitions of column heading titles
        ws.write(r-1, c-1, "Sex of reporter", self.col_heading_def)
        for _, sec_col_heading in YESNO:
            ws.merge_range(r-2, c, r-2, c+len(GENDER)-1, clean_title(sec_col_heading), self.sec_col_heading)
            for _, col_heading in GENDER:
                ws.write(r-1, c, clean_title(col_heading), self.col_heading)
                c += 1

        secondary_counts = OrderedDict()
        for sq_field, sq in SPECIAL_QUESTIONS.items():
            for yes_no, _ in YESNO:
                counts = Counter()
                for media_type, model in person_models.items():
                    sheet_name = model.sheet_name()
                    journalist_field_name = model._meta.get_field(model.sheet_name()).remote_field.model.journalist_field_name()
                    rows = model.objects \
                            .values(sq_field, f"{sheet_name}__{journalist_field_name}__sex", f"{sheet_name}__topic") \
                            .filter(**{f"{sheet_name}__country__in": self.country_list}) \
                            .exclude(**{sq_field: ""}) \
                            .filter(**{sq_field: yes_no}) \
                            .annotate(n=Count("id"))
                            
                    rows= self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        counts.update({(row["sex"], TOPIC_GROUPS[row['topic']]): row['n']})
       
                secondary_counts[yes_no] = counts

            self.write_primary_row_heading(ws, sq, r=r)
            self.tabulate_secondary_cols(ws, secondary_counts, GENDER, MAJOR_TOPICS, row_perc=False, write_primary_col_headins=False, write_col_headings=False, write_col_totals=False, r=r, raw_values=True)
            r += len(MAJOR_TOPICS)

    def ws_110(self, ws):
        """
        Cols: Rights 
        Rows: SQ 1,2,3, Major topic
        """
        r = 6
        c = 2
        # Write definitions of column heading titles
        ws.write(r-1, c-1, "Does this story make reference to gender equality or human rights", self.col_heading_def)
        for _, sec_col_heading in YESNO:
            ws.merge_range(r-2, c, r-2, c+len(YESNO)-1, clean_title(sec_col_heading), self.sec_col_heading)
            for _, col_heading in YESNO:
                ws.write(r-1, c, clean_title(col_heading), self.col_heading)
                c += 1

        secondary_counts = OrderedDict()
        for sq_field, sq in SPECIAL_QUESTIONS.items():
            for yes_no, _ in YESNO:
                counts = Counter()
                for media_type, model in person_models.items():
                    sheet_name = model.sheet_name()
                    rows = model.objects \
                            .values(sq_field, f"{sheet_name}__equality_rights", f"{sheet_name}__topic") \
                            .filter(**{f"{sheet_name}__country__in": self.country_list}) \
                            .exclude(**{sq_field: ""}) \
                            .filter(**{sq_field: yes_no}) \
                            .annotate(n=Count("id"))

                    rows= self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        counts.update({(row["equality_rights"], TOPIC_GROUPS[row['topic']]): row['n']})

                secondary_counts[yes_no] = counts

            self.write_primary_row_heading(ws, sq, r=r)
            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, MAJOR_TOPICS, row_perc=False, write_primary_col_headins=False, write_col_headings=False, write_col_totals=False, r=r, raw_values=True)
            r += len(MAJOR_TOPICS)

    def ws_111(self, ws):
        """
        Cols: Gender stereotypes
        Rows: SQ 1,2,3, Major topic
        """
        r = 6
        c = 2
        # Write definitions of column heading titles
        ws.write(r-1, c-1, "This story clearly challenges gender stereotypes", self.col_heading_def)
        for _, sec_col_heading in YESNO:
            ws.merge_range(r-2, c, r-2, c+len(AGREE_DISAGREE)-1, clean_title(sec_col_heading), self.sec_col_heading)
            for _, col_heading in AGREE_DISAGREE:
                ws.write(r-1, c, clean_title(col_heading), self.col_heading)
                c += 1

        secondary_counts = OrderedDict()
        for sq_field, sq in SPECIAL_QUESTIONS.items():
            for yes_no, _ in YESNO:
                counts = Counter()
                for media_type, model in person_models.items():
                    sheet_name = model.sheet_name()
                    rows = model.objects \
                            .values(sq_field, f"{sheet_name}__stereotypes", f"{sheet_name}__topic") \
                            .filter(**{f"{sheet_name}__country__in": self.country_list}) \
                            .exclude(**{sq_field: ""}) \
                            .filter(**{sq_field: yes_no}) \
                            .annotate(n=Count("id"))

                    rows= self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for row in rows:
                        counts.update({(row["stereotypes"], TOPIC_GROUPS[row['topic']]): row['n']})

                secondary_counts[yes_no] = counts

            self.write_primary_row_heading(ws, sq, r=r)
            self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=False, write_primary_col_headins=False, write_col_headings=False, write_col_totals=False, r=r, raw_values=True)
            r += len(MAJOR_TOPICS)

    def ws_s01(self, ws):
        """
        Cols: Sex of presenters, reporters and subjects
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()
        presenter_reporter = [('Presenter',[1, 3]), ('Reporter', [2])]

        for journo_type, role_ids in presenter_reporter:
            counts = Counter()

            if journo_type == 'Presenter':
                journo_models = broadcast_journalist_models
            elif journo_type == 'Reporter':
                journo_models = tm_journalist_models

            for media_type, model in journo_models.items():
                country = model.sheet_name() + '__country'

                rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    # Newspaper journos don't have roles
                    rows = rows.filter(role__in=role_ids)

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts[journo_type] = counts

        counts = Counter()
        for media_type, model in tm_person_models.items():
            country = model.sheet_name() + '__country'
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

        secondary_counts['Subjects'] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s02(self, ws):
        """
        Cols: Medium; Sex of subjects
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()

        for media_type, model in tm_person_models.items():
            counts = Counter()

            country = model.sheet_name() + '__country'
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts[media_type] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s03(self, ws):
        """
        Cols: Major topics; Sex
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()

            for media_type, model in tm_person_models.items():
                country = model.sheet_name() + '__country'
                topic = model.sheet_name() + '__topic'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(**{topic + '__in': topic_ids})\
                        .annotate(n=Count('id'))

                counts.update({(r['sex'], self.recode_country(r[country])): r['n'] for r in rows})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s04(self, ws):
        """
        Cols: Occupation; Sex
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()
        for occupation_id, occupation in OCCUPATION:
            counts = Counter()

            for media_type, model in tm_person_models.items():
                country = model.sheet_name() + '__country'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(occupation=occupation_id)\
                        .annotate(n=Count('id'))

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts[clean_title(occupation)] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s05(self, ws):
        """
        Cols: Function; Sex
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()
        for function_id, function in FUNCTION:
            counts = Counter()

            for media_type, model in tm_person_models.items():
                country = model.sheet_name() + '__country'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(function=function_id)\
                        .annotate(n=Count('id'))

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts[clean_title(function)] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s06(self, ws):
        """
        Cols: Victims; Sex
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()

        counts = Counter()
        for media_type, model in tm_person_models.items():
            country = model.sheet_name() + '__country'
            """
            Victim codes 0: Not applicable
                         9: Do not know
            """
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(victim_or_survivor='Y')\
                    .exclude(victim_of__in=[0,9])\
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})
        secondary_counts['Victim'] = counts

        counts = Counter()
        for media_type, model in tm_person_models.items():
            country = model.sheet_name() + '__country'
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(victim_or_survivor='N')\
                    .annotate(n=Count('id'))
            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

        for media_type, model in tm_person_models.items():
            country = model.sheet_name() + '__country'
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(victim_or_survivor='Y')\
                    .exclude(survivor_of__in=[0,9])\
                    .annotate(n=Count('id'))
            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

        secondary_counts['Not a victim'] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s07(self, ws):
        """
        Cols: Family status; Sex
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()

        for code, answer in YESNO:
            counts = Counter()
            for media_type, model in tm_person_models.items():
                country = model.sheet_name() + '__country'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(family_role=code)\
                        .annotate(n=Count('id'))

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts[answer] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s08(self, ws):
        """
        Cols: Quoted; Sex
        Rows: Country
        :: Newspaper only
        """
        secondary_counts = OrderedDict()
        model = person_models.get('Print')
        for code, answer in YESNO:
            counts = Counter()
            country = model.sheet_name() + '__country'
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(is_quoted=code)\
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})
            secondary_counts[answer] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s09(self, ws):
        """
        Cols: Photographed; Sex
        Rows: Country
        :: Newspaper only
        """
        secondary_counts = OrderedDict()
        model = person_models.get('Print')
        for code, answer in IS_PHOTOGRAPH:
            counts = Counter()
            country = model.sheet_name() + '__country'
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(is_photograph=code)\
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})
            secondary_counts[answer] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s10(self, ws):
        """
        Cols: Media; Journo Type; Sex
        Rows: Country
        :: Newspaper only
        """
        c = 1
        r = 8
        write_row_headings = True

        for media_type, model in tm_journalist_models.items():
            if media_type in broadcast_journalist_models:
                presenter_reporter = [('Presenter',[1, 3]), ('Reporter', [2])]
            else:
                # Newspaper journos don't have roles
                presenter_reporter = [('Reporter', [])]

            col = c + (1 if write_row_headings else 0)
            merge_range = (len(presenter_reporter) * len(self.male_female) * 2) - 1

            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(media_type), self.col_heading)

            secondary_counts = OrderedDict()

            for journo_type, role_ids in presenter_reporter:
                counts = Counter()
                country = model.sheet_name() + '__country'

                rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    # Newspaper journos don't have roles
                    rows = rows.filter(role__in=role_ids)

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})
                secondary_counts[journo_type] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, c=c, r=r, write_row_headings=write_row_headings, row_perc=True, show_N=True)

            c += (len(presenter_reporter) * len(self.male_female) * 2) + (1 if write_row_headings else 0)
            write_row_headings = False


    def ws_s11(self, ws):
        """
        Cols: Major topics; Sex
        Rows: Country
        :: Newspaper, television, radio
        """
        secondary_counts = OrderedDict()
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()

            for media_type, model in tm_journalist_models.items():
                country = model.sheet_name() + '__country'
                topic = model.sheet_name() + '__topic'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(**{topic + '__in': topic_ids})\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(role=REPORTERS)

                counts.update({(r['sex'], self.recode_country(r[country])): r['n'] for r in rows})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s12(self, ws):
        """
        Cols: Major topics; Women Central
        Rows: Country
        :: Newspaper, television, radio
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                .values('topic', 'country')\
                .filter(country__in=self.country_list)\
                .filter(about_women='Y')\
                .annotate(n=Count('id'))

            for row in rows:
                major_topic = TOPIC_GROUPS[row['topic']]
                counts.update({(major_topic, self.recode_country(row['country'])): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, self.countries, raw_values=True, write_col_totals=False)


    def ws_s13(self, ws):
        """
        Cols: Journalist Sex, Subject Sex
        Rows: Country
        :: Newspaper, television, radio
        """

        secondary_counts = OrderedDict()
        for sex_id, sex in self.male_female:
            counts = Counter()
            for media_type, model in tm_person_models.items():
                sheet_name = model.sheet_name()
                journo_name = model._meta.get_field(model.sheet_name()).remote_field.model.journalist_field_name()
                country = model.sheet_name() + '__country'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(**{sheet_name + '__' + journo_name + '__sex':sex_id})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(**{sheet_name + '__' + journo_name + '__role':REPORTERS})

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts[sex] = counts

        secondary_counts['col_title_def'] = [
            'Sex of reporter',
            'Sex of news subject']

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True)


    def ws_s14(self, ws):
        """
        Cols: Stereotypes
        Rows: Country
        :: Newspaper, television, radio
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                .values('stereotypes', 'country')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['stereotypes'], self.recode_country(row['country'])): row['n']})

        self.tabulate(ws, counts, AGREE_DISAGREE, self.countries, row_perc=True, show_N=True)


    def ws_s15(self, ws):
        """
        Cols: Gender inequality
        Rows: Country
        :: Newspaper, television, radio
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                .values('inequality_women', 'country')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['inequality_women'], self.recode_country(row['country'])): row['n']})

        self.tabulate(ws, counts, AGREE_DISAGREE, self.countries, row_perc=True, show_N=True)

    def ws_s16(self, ws):
        """
        Cols: Equality rights
        Rows: Country
        :: Newspaper, television, radio
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                .values('equality_rights', 'country')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['equality_rights'], self.recode_country(row['country'])): row['n']})

        self.tabulate(ws, counts, YESNO, self.countries, row_perc=True, show_N=True)


    def ws_s17(self, ws):
        """
        Cols: Sex of reporters and subjects
        Rows: Country
        :: Internet, Twitter
        """
        c = 1
        for media_type, model in dm_journalist_models.items():
            self.write_primary_row_heading(ws, media_type, c=c+1, r=4)

            secondary_counts = OrderedDict()
            counts = Counter()
            country = model.sheet_name() + '__country'

            rows = model.objects\
                .values('sex', country)\
                .filter(**{country + '__in': self.country_list})\
                .filter(sex__in=self.male_female_ids)\
                .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts['Reporter'] = counts

            counts = Counter()

            model =dm_person_models[media_type]
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            secondary_counts['Subjects'] = counts
            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

            c = ws.dim_colmax + 2


    def ws_s18(self, ws):
        """
        Cols: Sex of subjects
        Rows: Country
        :: Internet, Twitter
        """
        c = 1
        for media_type, model in dm_person_models.items():
            self.write_primary_row_heading(ws, media_type, c=c+1, r=4)

            counts = Counter()

            country = model.sheet_name() + '__country'
            rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

            self.tabulate(ws, counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=7)

            c = ws.dim_colmax + 2


    def ws_s19(self, ws):
        """
        Cols: Major topics; Sex
        Rows: Country
        :: Internet, Twitter
        """
        c = 1
        for media_type, model in dm_person_models.items():

            self.write_primary_row_heading(ws, media_type, c=c+1, r=4)
            secondary_counts = OrderedDict()

            for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
                counts = Counter()
                country = model.sheet_name() + '__country'
                topic = model.sheet_name() + '__topic'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(**{topic + '__in': topic_ids})\
                        .annotate(n=Count('id'))

                counts.update({(r['sex'], self.recode_country(r[country])): r['n'] for r in rows})

                major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
                secondary_counts[major_topic_name] = counts

                self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

            c = ws.dim_colmax + 2

    def ws_s20(self, ws):
        """
        Cols: Occupation; Sex
        Rows: Country
        :: Internet, Twitter
        """
        c = 1

        for media_type, model in dm_person_models.items():
            if not media_type == 'Twitter':
                self.write_primary_row_heading(ws, media_type, c=c+1, r=4)
                secondary_counts = OrderedDict()
                country = model.sheet_name() + '__country'

                for occupation_id, occupation in OCCUPATION:
                    counts = Counter()
                    rows = model.objects\
                            .values('sex', country)\
                            .filter(**{country + '__in': self.country_list})\
                            .filter(sex__in=self.male_female_ids)\
                            .filter(occupation=occupation_id)\
                            .annotate(n=Count('id'))

                    for row in rows:
                        counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

                    secondary_counts[clean_title(occupation)] = counts

                    self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

                c = ws.dim_colmax + 2


    def ws_s21(self, ws):
        """
        Cols: Function; Sex
        Rows: Country
        :: Internet, Twitter
        """
        c = 1

        for media_type, model in dm_person_models.items():
            if not media_type == 'Twitter':
                self.write_primary_row_heading(ws, media_type, c=c+1, r=4)
                secondary_counts = OrderedDict()
                country = model.sheet_name() + '__country'

                for function_id, function in FUNCTION:
                    counts = Counter()
                    rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(function=function_id)\
                        .annotate(n=Count('id'))

                    for row in rows:
                        counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

                    secondary_counts[clean_title(function)] = counts

                    self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

                c = ws.dim_colmax + 2

    def ws_s22(self, ws):
        """
        Cols: Victims; Sex
        Rows: Country
        :: Internet, Twitter
        """
        c = 1

        for media_type, model in dm_person_models.items():
            if not media_type == 'Twitter':
                self.write_primary_row_heading(ws, media_type, c=c+1, r=4)
                secondary_counts = OrderedDict()
                country = model.sheet_name() + '__country'

                counts = Counter()
                rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(victim_or_survivor='Y')\
                    .exclude(victim_of=0)\
                    .annotate(n=Count('id'))

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

                secondary_counts['Victim'] = counts

                counts = Counter()
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(victim_or_survivor='N')\
                        .annotate(n=Count('id'))
                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

                rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(victim_or_survivor='Y')\
                    .exclude(survivor_of=0)\
                    .annotate(n=Count('id'))
                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

                secondary_counts['Not a victim'] = counts

                self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

                c = ws.dim_colmax + 2


    def ws_s23(self, ws):
        """
        Cols: Quoted; Sex
        Rows: Country
        :: Internet, Twitter
        """
        c = 1

        for media_type, model in dm_person_models.items():
            if not media_type == 'Twitter':
                self.write_primary_row_heading(ws, media_type, c=c+1, r=4)
                secondary_counts = OrderedDict()
                country = model.sheet_name() + '__country'
                for code, answer in YESNO:
                    counts = Counter()
                    rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(is_quoted=code)\
                        .annotate(n=Count('id'))

                    for row in rows:
                        counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

                    secondary_counts[answer] = counts

                    self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

                c = ws.dim_colmax + 2


    def ws_s24(self, ws):
        """
        Cols: Photographed; Sex
        Rows: Country
        :: Internet, Twitter
        """
        c = 1

        for media_type, model in dm_person_models.items():

            self.write_primary_row_heading(ws, media_type, c=c+1, r=4)
            secondary_counts = OrderedDict()
            country = model.sheet_name() + '__country'
            for code, answer in IS_PHOTOGRAPH:
                counts = Counter()
                rows = model.objects\
                    .values('sex', country)\
                    .filter(**{country + '__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(is_photograph=code)\
                    .annotate(n=Count('id'))

                for row in rows:
                    counts.update({(row['sex'], self.recode_country(row[country])): row['n']})

                secondary_counts[answer] = counts

                self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

            c = ws.dim_colmax + 2


    def ws_s25(self, ws):
        """
        Cols: Major topics; Sex
        Rows: Country
        :: Internet, Twitter
        """
        c = 1
        for media_type, model in dm_journalist_models.items():

            self.write_primary_row_heading(ws, media_type, c=c+1, r=4)
            secondary_counts = OrderedDict()

            for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
                counts = Counter()
                country = model.sheet_name() + '__country'
                topic = model.sheet_name() + '__topic'
                rows = model.objects\
                        .values('sex', country)\
                        .filter(**{country + '__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(**{topic + '__in': topic_ids})\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(role=REPORTERS)

                counts.update({(r['sex'], self.recode_country(r[country])): r['n'] for r in rows})

                major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
                secondary_counts[major_topic_name] = counts

                self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.countries, row_perc=True, show_N=True, c=c, r=8)

            c = ws.dim_colmax + 2


    def ws_s26(self, ws):
        """
        Cols: Major topics; Women Central
        Rows: Country
        :: Internet, Twitter
        """
        c = 1
        for media_type, model in dm_sheet_models.items():
            self.write_primary_row_heading(ws, media_type, c=c+1, r=4)

            counts = Counter()
            rows = model.objects\
                .values('topic', 'country')\
                .filter(country__in=self.country_list)\
                .filter(about_women='Y')\
                .annotate(n=Count('id'))

            for row in rows:
                major_topic = TOPIC_GROUPS[row['topic']]
                counts.update({(major_topic, self.recode_country(row['country'])): row['n']})


            self.tabulate(ws, counts, MAJOR_TOPICS, self.countries, raw_values=True, c=c, r=7, write_col_totals=False)

            c = ws.dim_colmax + 2


    def ws_s27(self, ws):
        """
        Cols: Stereotypes
        Rows: Country
        :: Internet, Twitter
        """
        c = 1
        for media_type, model in dm_sheet_models.items():
            self.write_primary_row_heading(ws, media_type, c=c+1, r=4)

            counts = Counter()
            rows = model.objects\
                .values('stereotypes', 'country')\
                .filter(country__in=self.country_list)\
                .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['stereotypes'], self.recode_country(row['country'])): row['n']})


            self.tabulate(ws, counts, AGREE_DISAGREE, self.countries, raw_values=True, c=c, r=7, write_col_totals=False)

            c = ws.dim_colmax + 2
    
    def ws_s28(self, ws):
        """
        Cols: Sex of subject
        Rows: Country
        """
        counts = Counter()
        for _, model in person_models.items():
            sheet_name = model.sheet_name()
            country_field = f"{sheet_name}__country"
            rows = model.objects \
                    .values('sex', country_field) \
                    .filter(**{f"{sheet_name}__covid19": 1}) \
                    .filter(**{f"{country_field}__in": self.country_list}) \
                    .filter(sex__in=self.male_female_ids) \
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country_field])): row['n']})

        self.tabulate(ws, counts, self.male_female, self.countries, row_perc=True, show_N=True)

    def ws_s29(self, ws):
        """
        Cols: Sex of reporter
        Rows: Country
        """
        counts = Counter()
        for _, model in journalist_models.items():
            sheet_name = model.sheet_name()
            country_field = f"{sheet_name}__country"
            rows = model.objects \
                    .values('sex', country_field) \
                    .filter(**{f"{sheet_name}__covid19": 1}) \
                    .filter(**{f"{country_field}__in": self.country_list}) \
                    .filter(sex__in=self.male_female_ids) \
                    .annotate(n=Count('id'))

            for row in rows:
                counts.update({(row['sex'], self.recode_country(row[country_field])): row['n']})

        self.tabulate(ws, counts, self.male_female, self.countries, row_perc=True, show_N=True)

    def ws_sr01(self, ws):
        """
        Cols: Sex of presenters, reporters and subjects
        Rows: Country
        :: Newspaper, television, radio by region
        """
        secondary_counts = OrderedDict()
        presenter_reporter = [('Presenter',[1, 3]), ('Reporter', [2])]

        for journo_type, role_ids in presenter_reporter:
            counts = Counter()

            if journo_type == 'Presenter':
                journo_models = broadcast_journalist_models
            elif journo_type == 'Reporter':
                journo_models = tm_journalist_models

            for media_type, model in journo_models.items():
                region = model.sheet_name() + '__country_region__region'

                rows = model.objects\
                    .values('sex', region)\
                    .filter(**{region + '__in': self.all_region_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    # Newspaper journos don't have roles
                    rows = rows.filter(role__in=role_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                    counts.update({(row['sex'], region_id): row['n']})

            secondary_counts[journo_type] = counts

        counts = Counter()
        for media_type, model in tm_person_models.items():
            region = model.sheet_name() + '__country_region__region'
            rows = model.objects\
                    .values('sex', region)\
                    .filter(**{region + '__in': self.all_region_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                counts.update({(row['sex'], region_id): row['n']})

        secondary_counts['Subjects'] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)


    def ws_sr02(self, ws):
        """
        Cols: Major topics; Sex
        Rows: Country
        :: Newspaper, television, radio by region
        """
        secondary_counts = OrderedDict()
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()

            for media_type, model in tm_sheet_models.items():
                region = 'country_region__region'
                person_sex_field = '%s__sex' % model.person_field_name()
                rows = model.objects\
                        .values(person_sex_field, region)\
                        .filter(**{region + '__in': self.all_region_list})\
                        .filter(**{person_sex_field + '__in': self.male_female_ids})\
                        .filter(topic__in=topic_ids)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for row in rows:
                    region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                    counts.update({(row["sex"], region_id): row['n']})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)


    def ws_sr03(self, ws):
        """
        Cols: Function; Sex
        Rows: Country
        :: Newspaper, television, radio by region
        """
        secondary_counts = OrderedDict()
        for function_id, function in FUNCTION:
            counts = Counter()

            for media_type, model in tm_person_models.items():
                region = model.sheet_name() + '__country_region__region'
                rows = model.objects\
                        .values('sex', region)\
                        .filter(**{region + '__in': self.all_region_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .filter(function=function_id)\
                        .annotate(n=Count('id'))

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                    counts.update({(row['sex'], region_id): row['n']})

            secondary_counts[clean_title(function)] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)


    def ws_sr04(self, ws):
        """
        Cols: Photographed; Sex
        Rows: Country
        :: Newspaper only region
        """
        secondary_counts = OrderedDict()
        model = person_models.get('Print')

        for code, answer in IS_PHOTOGRAPH:
            counts = Counter()
            region = model.sheet_name() + '__country_region__region'
            rows = model.objects\
                    .values('sex', region)\
                    .filter(**{region + '__in': self.all_region_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .filter(is_photograph=code)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Print')

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                counts.update({(row['sex'], region_id): row['n']})


            secondary_counts[answer] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)


    def ws_sr05(self, ws):
        """
        Cols: Media; Journo Type; Sex
        Rows: Country
        :: Newspaper, television, radio by region
        """
        c = 1
        r = 8
        write_row_headings = True

        for media_type, model in journalist_models.items():
            if media_type in broadcast_journalist_models:
                presenter_reporter = [('Presenter',[1, 3]), ('Reporter', [2])]
            else:
                # Newspaper journos don't have roles
                presenter_reporter = [('Reporter', [])]

            col = c + (1 if write_row_headings else 0)
            merge_range = (len(presenter_reporter) * len(self.male_female) * 2) - 1

            ws.merge_range(r-4, col, r-4, col + merge_range, clean_title(media_type), self.col_heading)

            secondary_counts = OrderedDict()
            for journo_type, role_ids in presenter_reporter:
                counts = Counter()
                region = model.sheet_name() + '__country_region__region'

                rows = model.objects\
                        .values('sex', region)\
                        .filter(**{region + '__in': self.all_region_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    # Newspaper journos don't have roles
                    rows = rows.filter(role__in=role_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    region_id = [reg[0] for reg in self.all_regions if reg[1] == row["region"]][0]
                    counts.update({(row['sex'], region_id): row['n']})

                secondary_counts[journo_type] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True, c=c, r=r, write_row_headings=write_row_headings)

            c += (len(presenter_reporter) * len(self.male_female) * 2) + (1 if write_row_headings else 0)
            write_row_headings = False


    def ws_sr06(self, ws):
        """
        Cols: Major topics; Sex
        Rows: Country
        :: Newspaper, television, radio by region
        """
        secondary_counts = OrderedDict()
        for major_topic, topic_ids in GROUP_TOPICS_MAP.items():
            counts = Counter()
            for media_type, model in tm_sheet_models.items():

                region = 'country_region__region'
                journo_sex_field = '%s__sex' % model.journalist_field_name()
                journo_role_field = '%s__role' % model.journalist_field_name()

                rows = model.objects\
                    .values(journo_sex_field, region)\
                    .filter(**{region + '__in': self.all_region_list})\
                    .filter(**{journo_sex_field + '__in': self.male_female_ids})\
                    .filter(topic__in=topic_ids)\
                    .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    # Newspaper journos don't have roles
                    rows = rows.filter(**{journo_role_field: REPORTERS})

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for row in rows:
                    region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                    counts.update({(row["sex"], region_id): row['n']})

            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)


    def ws_sr07(self, ws):
        """
        Cols: Journalist Sex, Subject Sex
        Rows: Country
        :: Newspaper, television, radio by region
        """
        secondary_counts = OrderedDict()
        for sex_id, sex in self.male_female:
            counts = Counter()
            for media_type, model in tm_person_models.items():
                sheet_name = model.sheet_name()
                journo_name = model._meta.get_field(model.sheet_name()).remote_field.model.journalist_field_name()
                region = model.sheet_name() + '__country_region__region'
                rows = model.objects\
                        .values('sex', region)\
                        .filter(**{region + '__in': self.all_region_list})\
                        .filter(**{sheet_name + '__' + journo_name + '__sex':sex_id})\
                        .filter(sex__in=self.male_female_ids)\
                        .annotate(n=Count('id'))

                if media_type in REPORTER_MEDIA:
                    rows = rows.filter(**{sheet_name + '__' + journo_name + '__role':REPORTERS})

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                    counts.update({(row['sex'], region_id): row['n']})


            secondary_counts[sex] = counts

        secondary_counts['col_title_def'] = [
            'Sex of reporter',
            'Sex of news subject']

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, self.all_regions, row_perc=True, show_N=True)


    def ws_sr08(self, ws):
        """
        Cols: Major topics; Women Central
        Rows: Country
        :: Newspaper, television, radio by region
        """
        counts = Counter()
        region = 'country_region__region'
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                .values('topic', region)\
                .filter(**{region + '__in': self.all_region_list})\
                .filter(about_women='Y')\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, media_type)

            for row in rows:
                major_topic = TOPIC_GROUPS[row['topic']]
                region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                counts.update({(major_topic, region_id): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, self.all_regions, raw_values=True, write_col_totals=False)


    def ws_sr09(self, ws):
        """
        Cols: Gender inequality
        Rows: Country
        :: Newspaper, television, radio by region
        """
        counts = Counter()
        region = 'country_region__region'
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                .values('inequality_women', region)\
                .filter(**{region + '__in': self.all_region_list})\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, media_type)

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                counts.update({(row['inequality_women'], region_id): row['n']})

        self.tabulate(ws, counts, AGREE_DISAGREE, self.all_regions, row_perc=True, show_N=True)


    def ws_sr10(self, ws):
        """
        Cols: Stereotypes
        Rows: Country
        :: Newspaper, television, radio by region
        """
        counts = Counter()
        region = 'country_region__region'
        for media_type, model in tm_sheet_models.items():
            rows = model.objects\
                .values('stereotypes', region)\
                .filter(**{region + '__in': self.all_region_list})\
                .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model._meta.db_table, media_type)

            for row in rows:
                region_id = [r[0] for r in self.all_regions if r[1] == row["region"]][0]
                counts.update({(row['stereotypes'], region_id): row['n']})

        self.tabulate(ws, counts, AGREE_DISAGREE, self.all_regions, row_perc=True, show_N=True)

    # -------------------------------------------------------------------------------
    # Helper functions
    #
    def write_headers(self, ws, title, description):
        """
        Write the headers to the worksheet
        """
        ws.write(0, 0, title, self.heading)
        ws.write(1, 0, description, self.heading)
        ws.write(3, 2, self.current_year, self.heading)

    def write_col_headings(self, ws, cols, c=2, r=4, show_N=False):
        """
        :param ws: worksheet to write to
        :param cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param r, c: initial position where cursor should start writing to

        """
        if show_N:
            for col_id, col_title in cols:
                ws.write(r, c, clean_title(col_title), self.col_heading)
                ws.write(r + 1, c, "N")
                ws.write(r + 1, c + 1, "%")
                c += 2
        else:
            for col_id, col_title in cols:
                ws.write(r, c, clean_title(col_title), self.col_heading)
                ws.write(r + 1, c, "%")
                c += 1


    def write_primary_row_heading(self, ws, heading, c=0, r=6):
        """
        :param ws: worksheet to write to
        :param heading: row heading to write
        :param r, c: position where heading should be written to

        """
        ws.write(r, c, clean_title(heading), self.heading)

    def write_overall_value(self, ws, value, total, c, r, write_overall, overall_label = "Overall"):
        if total == 0:
            total = 1
        p_value = value / total
        if write_overall:
            ws.write(r, c-1, overall_label, self.label)
        ws.write(r, c, p_value, self.P)

    def tabulate_secondary_cols(self, ws, secondary_counts, cols, rows, row_perc=False, write_row_headings=True, write_primary_col_headins=True, write_col_headings=True, write_col_totals=True, filter_cols=None, c=1, r=7, show_N=False, raw_values=False):
        """
        :param ws: worksheet to write to
        :param secondary_counts: dict in following format:
            {'Primary column heading': Count object, ...}
        :param list cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param list rows: list of `(row_id, row_heading)` tuples of row ids and titles
        :param write_row_headings: See `tabulate` below.
        :param write_primary_col_headings: Should we write the primary col headings i.e. keys in `secondary_counts` dict.
        :param bool row_perc: should percentages by calculated by row instead of column (default: False)
        """

        write_row_totals = row_perc and not show_N

        # row titles
        if write_row_headings:
            for i, row in enumerate(rows):
                row_id, row_heading = row
                ws.write(r + i, c, clean_title(row_heading), self.label)
            c += 1

        if 'col_title_def' in secondary_counts:
            # Write definitions of column heading titles
            ws.write(r-3, c-1, secondary_counts['col_title_def'][0], self.sec_col_heading_def)
            ws.write(r-2, c-1, secondary_counts['col_title_def'][1], self.col_heading_def)
            secondary_counts.pop('col_title_def')

        # number of columns per secondary column
        sec_cols = len(filter_cols or cols)
        if show_N:
            sec_cols *= 2
        if not show_N and row_perc:
            sec_cols += 1

        for field, counts in secondary_counts.items():
            if write_primary_col_headins:
                if sec_cols > 1:
                    ws.merge_range(r-3, c, r-3, c+sec_cols-1, clean_title(field), self.sec_col_heading)
                else:
                    ws.write(r-3, c, clean_title(field), self.sec_col_heading)

            self.tabulate(ws, counts, cols, rows, row_perc=row_perc, write_row_headings=False,
                          write_col_headings=write_col_headings, write_row_totals=write_row_totals,
                          write_col_totals=write_col_totals, filter_cols=filter_cols, r=r, c=c,
                          show_N=show_N, raw_values=raw_values)
            c += sec_cols

    def tabulate(self, ws, counts, cols, rows, row_perc=False,
                 write_row_headings=True, write_col_headings=True, write_row_totals=True, write_col_totals=True,
                 filter_cols=None, c=1, r=6, show_N=False, raw_values=False, unweighted=False):
        """ Emit a table.

        :param ws: worksheet to write to
        :param dict counts: dict from `(col_id, row_id)` tuples to count for that combination.
        :param list cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param list rows: list of `(row_id, row_heading)` tuples of row ids and titles
        :param bool row_perc: should percentages by calculated by row instead of column (default: False)
        :param write_row_headings: Should we write the row headings. False if already written.
        :param write_row_totals: Should we write the row totals. False if tabultae_secondary_cols was run.
        :param write_col_total: write column totals?
        :param write_col_headings: Should we write the col headings. False if already written.
        :param filter_cols: If not None, display only passed subset of columns e.g. only female
        :param raw_values: calculate percentage based on values, or just use values?
        :param r, c: initial position where cursor should start writing to
        :param unweighted: values are unweighted? default: False
        """
        if row_perc:
            # Calc percentage by row
            row_totals = {}
            for row_id, row_heading in rows:
                row_totals[row_id] = sum(int(round(counts.get((col_id, row_id), 0))) for col_id, _ in cols)  # noqa

        # row titles
        if write_row_headings:
            # else already written
            for i, row in enumerate(rows):
                row_id, row_heading = row
                ws.write(r+i, c, clean_title(row_heading), self.label)
            c += 1

        # if only filtered results should be shown
        # e.g. only print female columns
        if filter_cols:
            cols = filter_cols

        title_N = "N"
        if unweighted:
            title_N = "N (raw)"

        if 'col_title_def' in counts and write_col_headings:
            # write definition of column headings
            ws.write(r-2, c-1, counts['col_title_def'], self.col_heading_def)
            counts.pop('col_title_def')

        # values, written column by column
        for col_id, col_heading in cols:
            # column title
            if write_col_headings:
                # else already written
                if show_N:
                    ws.merge_range(r-2, c, r-2, c+1, clean_title(col_heading), self.col_heading)
                    ws.write(r-1, c, "%", self.label)
                    ws.write(r-1, c+1, title_N, self.label)
                else:
                    ws.write(r-2, c, clean_title(col_heading), self.col_heading)
                    if raw_values:
                        ws.write(r-1, c, title_N, self.label)
                    else:
                        ws.write(r-1, c, "%", self.label)

            if not row_perc:
                # calculate column totals
                total = sum(int(round(counts.get((col_id, row_id), 0))) for row_id, _ in rows)

            # values for this column
            col_total = 0
            for i, row in enumerate(rows):
                row_id, row_title = row

                if row_perc:
                    # row totals
                    total = row_totals[row_id]

                n = int(round(counts.get((col_id, row_id), 0)))
                perc = p(n, total)
                col_total += perc

                if raw_values:
                    ws.write(r+i, c, n, self.N)
                else:
                    ws.write(r+i, c, perc, self.P)
                    if show_N:
                        ws.write(r+i, c+1, n, self.N)

            if write_col_totals and not row_perc:
                ws.write(r+i+1, c, col_total, self.P)

            c += 2 if show_N else 1

        if row_perc and write_row_totals:
            if write_col_headings:
                ws.write(r-1, c, title_N)

            # Write the row totals
            for i, row in enumerate(rows):
                row_id, row_title = row
                ws.write(r+i, c, row_totals[row_id], self.N)

    def tabulate_historical(self, ws, current_ws, cols, rows, c=None, r=6, write_row_headings=True,
                            write_col_headings=True, show_N_and_P=False, major_cols=None,
                            skip_major_col_heading=False, write_year=True, values_N=False):
        """
        Write historical data table.

        :param ws: worksheet to write to
        :param current_ws: name of the current period's worksheet
        :param cols: list of (id, key) column pairs
        :param rows: list of (id, key) row pairs
        :param c: column to start at; default: furtherst column to the right
        :param r: row to start at
        :param write_row_headings: should row headings be written?
        :param write_col_headings: should col headings be written?
        :param show_N_and_P: show both N and P for a row/col value, or just show P?
        :param major_cols: the major (top) columns as a list of (id, key) pairs
        :param skip_major_col_heading: allow space for, but skip, major column headings?
        :param write_year: should we write the year?
        :param values_N: are the values we're printing N or P values? (default: False)
        """
        if c is None:
            c = ws.dim_colmax + 2

        if values_N:
            formats = [self.N, self.N]
        else:
            formats = [self.P, self.N]

        try:
            country = self.country_list[0]
            region = self.region_list[0]

            historical_data = self.historical.get(current_ws, self.report_type, year=self.historical_year,
                                                  region=region, country=country)
        except KeyError as e:
            if self.report_type == 'global':
                raise e
            ws.write(r, c, "Historical data not available at the %s level." % self.report_type)
            self.log.warn(e)
            return

        years = sorted(historical_data.keys())

        if major_cols:
            r += 1

        values_per_col = 2 if show_N_and_P else 1

        if write_row_headings:
            # row titles
            for i, (row_id, row_heading) in enumerate(rows):
                row_heading = clean_title(row_heading)
                ws.write(r + i, c, row_heading)
            c += 1

        for year_i, year in enumerate(years):
            year_data = historical_data[year]

            if write_year:
                offset = 3
                if skip_major_col_heading or major_cols:
                    offset = 4
                ws.write(r - offset, c, year, self.heading)

            # for each major column heading
            for mcol_id, mcol_heading in (major_cols or [(None, None)]):
                if mcol_id is not None:
                    mcol_heading = clean_title(mcol_heading)
                    if canon(mcol_heading) not in year_data:
                        continue

                    if write_col_headings:
                        # major column title
                        width = len(cols) * values_per_col
                        if width > 1:
                            ws.merge_range(r - 3, c, r - 3, c + width - 1, mcol_heading, self.sec_col_heading)
                        else:
                            ws.write(r - 3, c, mcol_heading, self.sec_col_heading)

                    # get data
                    data = year_data[canon(mcol_heading)]
                else:
                    data = year_data

                # do we need to keep N aside as a special column?
                columns = cols
                if canon('N') in data:
                    columns = columns + [('N', 'N')]
                if canon('n_digital') in data:
                    columns = columns + [('N', 'n_digital')]

                # for each minor column heading
                for col_id, col_heading in columns:
                    col_heading = clean_title(col_heading)

                    if canon(col_heading) not in data:
                        continue

                    # column title
                    value_formats = formats
                    if write_col_headings:
                        if col_heading != 'N' and col_heading !='n_digital':
                            if values_per_col > 1:
                                ws.merge_range(r - 2, c, r - 2, c + values_per_col - 1, col_heading, self.col_heading)
                            else:
                                ws.write(r - 2, c, col_heading, self.col_heading)

                            ws.write(r - 1, c, '%', self.label)
                            # if multiple values for this column, we're writing both a
                            # percentage and an N
                            if show_N_and_P:
                                ws.write(r - 1, c + 1, 'N', self.label)

                        else:
                            ws.write(r - 1, c, 'N', self.label)
                            value_formats = [self.N, self.N]

                    # row values
                    for i, (row_id, row_heading) in enumerate(rows):
                        row_heading = clean_title(row_heading)
                        value = data[canon(col_heading)].get(canon(row_heading))

                        if value is None:
                            # check if it's due to having % and N
                            p = data.get(canon(col_heading), {}).get('%', {})
                            n = data.get(canon(col_heading), {}).get('n', {})
                            if (p or n):
                                value = [p.get(canon(row_heading), "n/a"), n.get(canon(row_heading), "n/a")]
                            else:
                                value = ['n/a'] * values_per_col
                        elif not isinstance(value, list):
                            value = [value]

                        for v in range(values_per_col):
                            ws.write(r + i, c + v, value[v], value_formats[v])

                    # for next column
                    c += values_per_col
