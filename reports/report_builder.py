# Python
import StringIO
from collections import Counter, OrderedDict

# Django
from django_countries import countries
from django.db import connection
from django.db.models import Count, FieldDoesNotExist

# 3rd Party
import xlsxwriter

# Project
from forms.models import (
    NewspaperSheet, NewspaperPerson, TelevisionJournalist,
    person_models, sheet_models, journalist_models,
    tm_person_models, tm_sheet_models, tm_journalist_models,
    dm_person_models, dm_sheet_models, dm_journalist_models,)
from forms.modelutils import (TOPICS, GENDER, SPACE, OCCUPATION, FUNCTION, SCOPE,
    YESNO, AGES, SOURCE, VICTIM_OF, SURVIVOR_OF, IS_PHOTOGRAPH, AGREE_DISAGREE,
    RETWEET, TV_ROLE, MEDIA_TYPES, TM_MEDIA_TYPES, DM_MEDIA_TYPES, CountryRegion)
from report_details import WS_INFO, REGION_COUNTRY_MAP, MAJOR_TOPICS, TOPIC_GROUPS, GROUP_TOPICS_MAP, FORMATS, FOCUS_TOPICS, FOCUS_TOPIC_MAP
from reports.models import Weights

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
    u'B1': u'BE',  # Belgium - French -> Belgium
    u'B2': u'BE',  # Belgium - English -> Belgium
    u'EN': u'UK',  # England -> United Kingdom
    u'IE': u'UK',  # Ireland -> United Kingdom
    u'SQ': u'UK',  # Scotland -> United Kingdom
    u'WL': u'UK',  # Wales -> United Kingdom
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

def get_regions():
    """
    Return a (id, region_name) list for all regions
    """
    country_regions = CountryRegion.objects\
                        .values('region')\
                        .exclude(region='Unmapped')
    regions = set(item['region'] for item in country_regions)
    return [(i, region) for i, region in enumerate(regions)]

def get_countries():
    """
    Return a (code, country) list for countries captured.
    """
    captured_country_codes = set()
    for model in sheet_models.itervalues():
        rows = model.objects.values('country')
        captured_country_codes.update([r['country'] for r in rows])
    return [(code, name) for code, name in list(countries) if code in captured_country_codes]

def get_region_countries(region):
    """
    Return a (code, country) list for a region.
    """
    if region == 'ALL':
        return get_countries()
    else:
        country_codes = REGION_COUNTRY_MAP[region]
        return [(code, name) for code, name in list(countries) if code in country_codes]

def get_country_region(country):
    """
    Return a (id, region_name) list to which a country belongs.
    """
    if country == 'ALL':
        return get_regions()
    else:
        return [(0, [k for k, v in REGION_COUNTRY_MAP.items() if country in v][0])]

def clean_title(text):
    """
    Return the string passed in stripped of its numbers and parentheses
    """
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
        return "station_name"
    elif media_type == "Radio":
        return "station_name"


class XLSXReportBuilder:
    def __init__(self, form):
        from reports.views import CountryForm, RegionForm
        self.form = form
        if isinstance(form, CountryForm):
            self.countries = form.filter_countries()
            self.regions = get_country_region(form.cleaned_data['country'])
            self.report_type = 'country'
        elif isinstance(form, RegionForm):
            region = [name for i, name in form.REGIONS if str(i) == form.cleaned_data['region']][0]
            self.countries = get_region_countries(region)
            self.regions = [(0, region)]
            self.report_type = 'region'
        else:
            self.countries = get_countries()
            self.regions = get_regions()
            self.report_type = 'global'

        self.country_list = [code for code, name in self.countries]
        self.region_list = [name for id, name in self.regions]

        if self.report_type == 'global':
            self.recode_countries()

        # Various utilities used for displaying details
        self.male_female = [(id, value) for id, value in GENDER if id in [1, 2]]
        self.male_female_ids = [id for id, value in self.male_female]
        self.female = [(id, value) for id, value in GENDER if id == 1]
        self.yes = [(id, value) for id, value in YESNO if id == 'Y']

        self.gmmp_year = '2015'

    def recode_countries(self):
        # squash recoded countries
        self.countries = [(c, n) for c, n in self.countries if c not in COUNTRY_RECODES]
        # add UK and Belgium
        self.countries.append((u'BE', u'Belgium - French and Flemish'))
        self.countries.append((u'UK', u'United Kingdom - England, Ireland, Scotland and Wales'))
        self.countries.sort(key=lambda p: p[1])

    def build(self):
        """
        Generate an Excel spreadsheet and return it as a string.
        """
        output = StringIO.StringIO()
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

        # Use the following for specifying which reports to create during dev
        # test_functions = [
        #     'ws_01', 'ws_02', 'ws_04', 'ws_05', 'ws_06', 'ws_07', 'ws_08', 'ws_09', 'ws_10',
        #     'ws_11', 'ws_12', 'ws_13', 'ws_14', 'ws_15', 'ws_16', 'ws_17', 'ws_18', 'ws_19', 'ws_20',
        #     'ws_21', 'ws_23', 'ws_24', 'ws_25', 'ws_26', 'ws_27', 'ws_28', 'ws_29', 'ws_30',
        #     'ws_31', 'ws_32', 'ws_34', 'ws_35', 'ws_36', 'ws_38', 'ws_39', 'ws_40',
        #     'ws_41', 'ws_42', 'ws_43', 'ws_44', 'ws_45', 'ws_46', 'ws_47', 'ws_48',
        #     'ws_49', 'ws_50', 'ws_51', 'ws_52', 'ws_53', 'ws_54', 'ws_55', 'ws_56', 'ws_57', 'ws_58', 'ws_59', 'ws_60',
        #     'ws_61', 'ws_62', 'ws_63', 'ws_64', 'ws_65', 'ws_66', 'ws_67', 'ws_68', 'ws_68b',
        #     'ws_75', 'ws_76', 'ws_77', 'ws_78']

        test_functions = ['ws_74', 'ws_75', 'ws_76', 'ws_77', 'ws_78']

        sheet_info = OrderedDict(sorted(WS_INFO.items(), key=lambda t: t[0]))

        for function in test_functions:
            if self.report_type in sheet_info[function]['reports']:
                ws = workbook.add_worksheet(sheet_info[function]['name'])
                self.write_headers(ws, sheet_info[function]['title'], sheet_info[function]['desc'])
                getattr(self, function)(ws)

        # -------------------------------------------------------------------

        # To ensure ordered worksheets
        # sheet_info = OrderedDict(sorted(WS_INFO.items(), key=lambda t: t[0]))

        # for ws_num, ws_info in sheet_info.iteritems():
        #     if self.report_type in ws_info['reports']:
        #         ws = workbook.add_worksheet(ws_info['name'])
        #         self.write_headers(ws, ws_info['title'], ws_info['desc'])
        #         getattr(self, ws_num)(ws)

        workbook.close()
        output.seek(0)

        return output.read()

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
            dict(zip([col[0] for col in desc], row))
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
        raw_query = raw_query.replace('SELECT', 'SELECT cast(round(SUM(reports_weights.weight)) as int) AS "n",')
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
            for media_type, model in models.iteritems():
                rows = model.objects\
                        .values('country_region__region')\
                        .filter(country_region__region__in=self.region_list)

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

    def ws_02(self, ws):
        """
        Cols: Media Type
        Rows: Region, Country
        """
        r = 6
        c = 2
        for media_types, models in SHEET_MEDIA_GROUPS:
            self.write_col_headings(ws, media_types, c=c)
            c += len(media_types) + 2

        weights = {(w.country, w.media_type): w.weight for w in Weights.objects.all()}

        for region_id, region in self.regions:
            counts_list = []
            for media_types, models in SHEET_MEDIA_GROUPS:

                counts = Counter()
                for media_type, model in models.iteritems():
                    name_field = get_sheet_model_name_field(media_type)
                    rows = model.objects\
                            .values(name_field, 'country')\
                            .filter(country__in=self.country_list)\
                            .annotate()

                    # rows = self.apply_distinct_weights(rows, model._meta.db_table, media_type)
                    for row in rows:
                        if row['country'] is not None:
                            weight = weights[(row['country'], media_type)]
                            # Get media id's to assign to counts
                            media_id = [media[0] for media in media_types if media[1] == media_type][0]
                            counts.update({(media_id, self.recode_country(row['country'])): weight})
                    for key, value in counts.iteritems():
                        counts[key] = int(round(value))
                counts_list.append(counts)

            self.write_primary_row_heading(ws, region, r=r)
            region_countries = [(code, country) for code, country in self.countries if code in REGION_COUNTRY_MAP[region]]
            self.tabulate(ws, counts_list[0], TM_MEDIA_TYPES, region_countries, row_perc=True, write_col_headings=False, r=r)
            c = 7
            self.tabulate(ws, counts_list[1], DM_MEDIA_TYPES, region_countries, row_perc=True, write_col_headings=False, write_row_headings=False, r=r, c=c)
            r += (len(region_countries) + 2)

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
                for media_type, model in models.iteritems():
                    rows = model.objects\
                            .values('topic')\
                            .filter(country_region__region=region)

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    for r in rows:
                        # Get media id's to assign to counts
                        media_id = [media[0] for media in media_types if media[1] == media_type][0]
                        major_topic = TOPIC_GROUPS[r['topic']]
                        counts.update({(media_id, major_topic): r['n']})
                secondary_counts[region] = counts
            counts_list.append(secondary_counts)

        self.tabulate_secondary_cols(ws, counts_list[0], TM_MEDIA_TYPES, MAJOR_TOPICS, row_perc=False)
        c = ws.dim_colmax + 2
        self.tabulate_secondary_cols(ws, counts_list[1], DM_MEDIA_TYPES, MAJOR_TOPICS, row_perc=False, c=c)

    def ws_05(self, ws):
        """
        Cols: Subject sex
        Rows: Major Topic
        """
        counts_list = []
        for media_types, models in PERSON_MEDIA_GROUPS:
            secondary_counts = OrderedDict()
            for media_type, model in models.iteritems():
                counts = Counter()
                topic_field = '%s__topic' % model.sheet_name()

                rows = model.objects\
                    .values('sex', topic_field)\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)
                for r in rows:
                    counts.update({(r['sex'], TOPIC_GROUPS[r['topic']]): r['n']})

                if media_type == "Internet":
                    secondary_counts["Internet"] = counts
                elif media_type == "Twitter":
                    secondary_counts["Twitter"] = counts
                else:
                    if "Print, Radio, Television" in secondary_counts:
                        secondary_counts["Print, Radio, Television"].update(counts)
                    else:
                        secondary_counts["Print, Radio, Television"] = counts

            counts_list.append(secondary_counts)
        self.tabulate_secondary_cols(ws, counts_list[0], self.male_female, MAJOR_TOPICS, row_perc=True)
        c = ws.dim_colmax + 2
        self.tabulate_secondary_cols(ws, counts_list[1], self.male_female, MAJOR_TOPICS, row_perc=True, c=c, write_row_headings=False)

    def ws_06(self, ws):
        """
        Cols: Region, Subject sex: female only
        Rows: Major Topics
        """
        counts_list = []
        for media_types, models in PERSON_MEDIA_GROUPS:
            secondary_counts = OrderedDict()
            for region_id, region in self.regions:
                counts = Counter()
                for media_type, model in models.iteritems():
                    topic_field = '%s__topic' % model.sheet_name()
                    rows = model.objects\
                        .values('sex', topic_field)\
                        .filter(**{model.sheet_name() + '__country_region__region':region})\
                        .filter(sex__in=self.male_female_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        counts.update({(r['sex'], TOPIC_GROUPS[r['topic']]): r['n']})
                secondary_counts[region] = counts
            counts_list.append(secondary_counts)

        self.tabulate_secondary_cols(ws, counts_list[0], self.male_female, MAJOR_TOPICS, row_perc=True, filter_cols=self.female, show_N=True)
        c = ws.dim_colmax + 2
        self.tabulate_secondary_cols(ws, counts_list[1], self.male_female, MAJOR_TOPICS, row_perc=True, c=c, filter_cols=self.female, show_N=True)

    def ws_07(self, ws):
        """
        Cols: Media Type
        Rows: Subject Sex
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            rows = model.objects\
                    .values('sex')\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            for r in rows:
                # Get media id's to assign to counts
                media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                counts.update({(media_id, r['sex']): r['n']})

        self.tabulate(ws, counts, TM_MEDIA_TYPES, self.male_female, row_perc=False)

    def ws_08(self, ws):
        """
        Cols: Subject Sex
        Rows: Scope
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            if 'scope' in model.sheet_field().rel.to._meta.get_all_field_names():
                scope = '%s__scope' % model.sheet_name()
                rows = model.objects\
                        .values('sex', scope)\
                        .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['scope']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, SCOPE, row_perc=True, filter_cols=self.female)

    def ws_09(self, ws):
        """
        Cols: Subject Sex
        Rows: Topic
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            topic = '%s__topic' % model.sheet_name()
            rows = model.objects\
                    .values('sex', topic)\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            counts.update({(r['sex'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, TOPICS, row_perc=True, filter_cols=self.female)

    def ws_10(self, ws):
        """
        Cols: Space
        Rows: Minor Topics
        :: Newspaper Sheets only
        """
        # Calculate row values for column
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            if media_type == 'Print':
                rows = model.objects\
                        .values('space', 'topic')\
                        .filter(country__in=self.country_list)

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for r in rows:
                    counts.update({(r['space'], TOPIC_GROUPS[r['topic']]): r['n']})

        self.tabulate(ws, counts, SPACE, MAJOR_TOPICS, row_perc=False)

    def ws_11(self, ws):
        """
        Cols: Equality Rights
        Rows: Major Topics
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.iteritems():
            if 'equality_rights' in model._meta.get_all_field_names():
                rows = model.objects\
                    .values('equality_rights', 'topic')\
                    .filter(country__in=self.country_list)

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for r in rows:
                    counts.update({(r['equality_rights'], TOPIC_GROUPS[r['topic']]): r['n']})

        self.tabulate(ws, counts, YESNO, MAJOR_TOPICS, row_perc=True)

    def ws_12(self, ws):
        """
        Cols: Region, Equality Rights
        Rows: Major Topics
        """
        secondary_counts = OrderedDict()
        for region_id, region_name in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.iteritems():
                # Some models has no equality rights field
                if 'equality_rights' in model._meta.get_all_field_names():
                    rows = model.objects\
                        .values('equality_rights', 'topic')\
                        .filter(country_region__region=region_name)

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    for r in rows:
                        counts.update({(r['equality_rights'], TOPIC_GROUPS[r['topic']]): r['n']})
            secondary_counts[region_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, MAJOR_TOPICS, row_perc=True)

    def ws_13(self, ws):
        """
        Cols: Journalist Sex, Equality Rights
        Rows: Topics
        """
        secondary_counts = OrderedDict()
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.iteritems():
                if 'equality_rights' in model.sheet_field().rel.to._meta.get_all_field_names():
                    topic = '%s__topic' % model.sheet_name()
                    equality_rights = '%s__equality_rights' % model.sheet_name()
                    rows = model.objects\
                            .values(equality_rights, topic)\
                            .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                            .filter(sex=gender_id)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        counts.update({(r['equality_rights'], TOPIC_GROUPS[r['topic']]): r['n']})
            secondary_counts[gender] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, MAJOR_TOPICS, row_perc=True)

    def ws_14(self, ws):
        """
        Cols: Sex
        Rows: Occupation
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            # some Person models don't have an occupation field
            if 'occupation' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'occupation')\
                        .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, OCCUPATION, row_perc=True, filter_cols=self.female)

    def ws_15(self, ws):
        """
        Cols: Sex
        Rows: Function
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            # some Person models don't have a function field
            if 'function' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'function')\
                        .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['function']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, FUNCTION, row_perc=True, filter_cols=self.female)

    def ws_16(self, ws):
        """
        Cols: Function, Sex
        Rows: Occupation
        """
        secondary_counts = OrderedDict()
        for function_id, function in FUNCTION:
            counts = Counter()
            for media_type, model in tm_person_models.iteritems():
                if 'function' in model._meta.get_all_field_names() and 'occupation' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('sex', 'occupation')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(function=function_id)\
                            .filter(sex__in=self.male_female_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})
            secondary_counts[function] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, OCCUPATION, row_perc=False)

    def ws_17(self, ws):
        """
        Cols: Age, Sex of Subject
        Rows: Function
        """
        secondary_counts = OrderedDict()
        for age_id, age in AGES:
            counts = Counter()
            for media_type, model in tm_person_models.iteritems():
                if 'function' in model._meta.get_all_field_names() and 'age' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('sex', 'function')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(age=age_id)\
                            .filter(sex__in=self.male_female_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['sex'], r['function']): r['n'] for r in rows})
            secondary_counts[age] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, FUNCTION, row_perc=False)

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
                .filter(sex__in=self.male_female_ids)

        rows = self.apply_weights(rows, NewspaperPerson.sheet_db_table(), 'Print')
        counts.update({(r['sex'], r['age']): r['n'] for r in rows})
        self.tabulate(ws, counts, self.male_female, AGES, row_perc=True)

    def ws_19(self, ws):
        """
        Cols: Sex
        Rows: Age
        :: Only for broadcast
        """
        counts = Counter()
        broadcast = ['Television']
        for media_type, model in person_models.iteritems():
             if media_type in broadcast:
                rows = model.objects\
                        .values('sex', 'age')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, AGES, row_perc=True)

    def ws_20(self, ws):
        """
        Cols: Function, Sex
        Rows: Occupation
        """
        secondary_counts = OrderedDict()
        functions_count = Counter()
        # Get top 5 functions
        for media_type, model in tm_person_models.iteritems():
            if 'function' in model._meta.get_all_field_names() and 'occupation' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('function')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                functions_count.update({(r['function']): r['n'] for r in rows})

        top_5_function_ids = [id for id, count in sorted(functions_count.items(), key=lambda x: -x[1])[:5]]
        top_5_functions = [(id, func) for id, func in FUNCTION if id in top_5_function_ids]

        for func_id, function in top_5_functions:
            counts = Counter()
            for media_type, model in tm_person_models.iteritems():
                if 'function' in model._meta.get_all_field_names() and 'occupation' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('sex', 'occupation')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(function=func_id)\
                            .filter(sex__in=self.male_female_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})
            secondary_counts[function] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, OCCUPATION, row_perc=False)

    def ws_21(self, ws):
        """
        Cols: Subject Sex
        Rows: Victim type
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            if 'victim_of' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'victim_of')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)\
                        .exclude(victim_of=None)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['victim_of']): r['n'] for r in rows})
        self.tabulate(ws, counts, self.male_female, VICTIM_OF, row_perc=False)

    def ws_23(self, ws):
        """
        Cols: Subject Sex
        Rows: Survivor type
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            if 'survivor_of' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'survivor_of')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .exclude(survivor_of=None)\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['survivor_of']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, SURVIVOR_OF, row_perc=False)

    def ws_24(self, ws):
        """
        Cols: Subject Sex
        Rows: Family Role
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            if 'family_role' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'family_role')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['family_role']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, YESNO, row_perc=False)

    def ws_25(self, ws):
        """
        Cols: Journalist Sex, Subject Sex
        Rows: Family Role
        """
        secondary_counts = OrderedDict()
        for sex_id, sex in self.male_female:
            counts = Counter()
            for media_type, model in tm_person_models.iteritems():
                if 'family_role' in model._meta.get_all_field_names():
                    sheet_name = model.sheet_name()
                    journo_name = model._meta.get_field(model.sheet_name()).rel.to.journalist_field_name()
                    rows = model.objects\
                            .values('sex', 'family_role')\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(**{sheet_name + '__' + journo_name + '__sex':sex_id})\
                            .filter(sex__in=self.male_female_ids)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['sex'], r['family_role']): r['n'] for r in rows})
            secondary_counts[sex] = counts

        secondary_counts['col_title_def'] = [
            'Sex of reporter',
            'Sex of news subject']

        self.tabulate_secondary_cols(ws, secondary_counts, self.male_female, YESNO, row_perc=False)

    def ws_26(self, ws):
        """
        Cols: Subject Sex
        Rows: Whether Quoted
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            if 'is_quoted' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'is_quoted')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['is_quoted']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, YESNO, row_perc=False)

    def ws_27(self, ws):
        """
        Cols: Subject Sex
        Rows: Photographed
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            if 'is_photograph' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'is_photograph')\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['is_photograph']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, IS_PHOTOGRAPH, row_perc=False)

    def ws_28(self, ws):
        """
        Cols: Medium
        Rows: Region
        :: Female reporters only
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.iteritems():
            region = model.sheet_name() + '__country_region__region'
            rows = model.objects\
                    .values(region)\
                    .filter(sex=1)\
                    .filter(**{region + '__in': self.region_list})

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            for row in rows:
                # Get media and region id's to assign to counts
                media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                region_id = [r[0] for r in self.regions if r[1] == row['region']][0]

                counts.update({(media_id, region_id): row['n']})

        self.tabulate(ws, counts, TM_MEDIA_TYPES, self.regions, row_perc=True)

    def ws_29(self, ws):
        """
        Cols: Regions
        Rows: Scope
        :: Female reporters only
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.iteritems():
            sheet_name = model.sheet_name()
            region = sheet_name + '__country_region__region'
            scope =  sheet_name + '__scope'
            if 'scope' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values(region, scope)\
                        .filter(**{region + '__in': self.region_list})\
                        .filter(sex=1)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    region_id = [r[0] for r in self.regions if r[1] == row['region']][0]
                    counts.update({(region_id, row['scope']): row['n']})

        self.tabulate(ws, counts, self.regions, SCOPE, row_perc=False)

    def ws_30(self, ws):
        """
        Cols: Region
        Rows: Major Topics
        :: Female reporters only
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.iteritems():
            sheet_name = model.sheet_name()
            region = sheet_name + '__country_region__region'
            topic =  sheet_name + '__topic'
            if 'topic' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values(region, topic)\
                        .filter(**{region + '__in': self.region_list})\
                        .filter(sex=1)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    region_id = [r[0] for r in self.regions if r[1] == row['region']][0]
                    major_topic = TOPIC_GROUPS[row['topic']]
                    counts.update({(region_id, major_topic): row['n']})

        self.tabulate(ws, counts, self.regions, MAJOR_TOPICS, row_perc=False)

    def ws_31(self, ws):
        """
        Cols: Sex of Reporter
        Rows: Minor Topics
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.iteritems():
            sheet_name = model.sheet_name()
            topic =  sheet_name + '__topic'
            if 'topic' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', topic)\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, TOPICS, row_perc=True, filter_cols=self.female)

    def ws_32(self, ws):
        """
        Cols: Medium
        Rows: Topics
        :: Female reporters only
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.iteritems():
            sheet_name = model.sheet_name()
            topic =  sheet_name + '__topic'
            if 'topic' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values(topic)\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex=1)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for row in rows:
                    media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                    counts.update({(media_id, row['topic']): row['n']})

        self.tabulate(ws, counts, TM_MEDIA_TYPES, TOPICS, row_perc=False)

    def ws_34(self, ws):
        """
        Cols: Sex of reporter
        Rows: Sex of subject
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            sheet_name = model.sheet_name()
            journo_name = model._meta.get_field(model.sheet_name()).rel.to.journalist_field_name()
            journo_sex = sheet_name + '__' + journo_name + '__sex'
            rows = model.objects\
                    .extra(select={"subject_sex": model._meta.db_table + ".sex"})\
                    .values(journo_sex, 'subject_sex')\
                    .filter(**{model.sheet_name() + '__country__in': self.country_list})\
                    .filter(sex__in=self.male_female_ids)\
                    .annotate(n=Count('id'))

            rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

            counts.update({(r['sex'], r['subject_sex']): r['n'] for r in rows})
        counts['col_title_def'] = 'Sex of reporter'

        self.tabulate(ws, counts, self.male_female, GENDER, row_perc=True, filter_cols=self.female)

    def ws_35(self, ws):
        """
        Cols: Sex of reporter
        Rows: Age of reporter
        :: Only for television
        """
        counts = Counter()
        rows = TelevisionJournalist.objects\
                .values('sex', 'age')\
                .filter(television_sheet__country__in=self.country_list)\
                .filter(sex__in=self.male_female_ids)

        rows = self.apply_weights(rows, TelevisionJournalist.sheet_db_table(), 'Television')
        counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, AGES, row_perc=True, filter_cols=self.female)

    def ws_36(self, ws):
        """
        Cols: Sex of Reporter
        Rows: Focus: about women
        """
        counts = Counter()
        for media_type, model in tm_journalist_models.iteritems():
            sheet_name = model.sheet_name()
            about_women =  sheet_name + '__about_women'
            if 'about_women' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', about_women)\
                        .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                        .filter(sex__in=self.male_female_ids)

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                counts.update({(r['sex'], r['about_women']): r['n'] for r in rows})

        self.tabulate(ws, counts, self.male_female, YESNO, row_perc=False)

    def ws_38(self, ws):
        """
        Cols: Focus: about women
        Rows: Major Topics
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.iteritems():
            if 'about_women' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('about_women', 'topic')\
                        .filter(country__in=self.country_list)

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                for r in rows:
                    counts.update({(r['about_women'], TOPIC_GROUPS[r['topic']]): r['n']})

        self.tabulate(ws, counts, YESNO, MAJOR_TOPICS, row_perc=True)

    def ws_39(self, ws):
        """
        Cols: Focus: about women
        Rows: Topics
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.iteritems():
            if 'about_women' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('about_women', 'topic')\
                        .filter(country__in=self.country_list)

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                counts.update({(r['about_women'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, YESNO, TOPICS, row_perc=True)

    def ws_40(self, ws):
        """
        Cols: Region, Topics
        Rows: Focus: about women
        """
        secondary_counts = OrderedDict()
        for region_id, region in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.iteritems():
                if 'about_women' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('topic', 'about_women')\
                            .filter(country_region__region=region)

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    counts.update({(r['about_women'], r['topic']): r['n'] for r in rows})
            secondary_counts[region] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, TOPICS, row_perc=False, filter_cols=self.yes)

    def ws_41(self, ws):
        """
        Cols: Equality rights raised
        Rows: Topics
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.iteritems():
            if 'equality_rights' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('equality_rights', 'topic')\
                        .filter(country__in=self.country_list)

                rows = self.apply_weights(rows, model._meta.db_table, media_type)

                counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
        self.tabulate(ws, counts, YESNO, TOPICS, row_perc=False)

    def ws_42(self, ws):
        """
        Cols: Region, Equality rights raised
        Rows: Topics
        """
        secondary_counts = OrderedDict()
        for region_id, region in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.iteritems():
                if 'equality_rights' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('topic', 'equality_rights')\
                            .filter(country_region__region=region)

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
            secondary_counts[region] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, TOPICS, row_perc=True)

    def ws_43(self, ws):
        """
        Cols: Sex of reporter, Equality rights raised
        Cols: Topics
        """
        secondary_counts = OrderedDict()
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.iteritems():
                sheet_name = model.sheet_name()
                topic = sheet_name + '__topic'
                equality_rights =  sheet_name + '__equality_rights'
                if 'equality_rights' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                    rows = model.objects\
                            .values(topic, equality_rights)\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                            .filter(sex=gender_id)

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
            secondary_counts[gender] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, TOPICS, row_perc=True)

    def ws_44(self, ws):
        """
        Cols: Sex of reporter, Equality rights raised
        Rows: Region
        """
        secondary_counts = OrderedDict()
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.iteritems():
                sheet_name = model.sheet_name()
                region = sheet_name + '__country_region__region'
                equality_rights =  sheet_name + '__equality_rights'
                if 'equality_rights' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                    rows = model.objects\
                            .values(equality_rights, region)\
                            .filter(sex=gender_id)\
                            .filter(**{region + '__in':self.region_list})

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        region_id = [id for id, name in self.regions if name == r['region']][0]
                        counts.update({(r['equality_rights'], region_id): r['n']})
            secondary_counts[gender] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.regions, row_perc=True)

    def ws_45(self, ws):
        """
        Cols: Sex of news subject
        Rows: Region
        :: Equality rights raised == Yes
        """
        counts = Counter()
        for media_type, model in tm_person_models.iteritems():
            if 'equality_rights' in model.sheet_field().rel.to._meta.get_all_field_names():
                region = model.sheet_name() + '__country_region__region'
                equality_rights = model.sheet_name() + '__equality_rights'
                rows = model.objects\
                        .values('sex', region)\
                        .filter(**{region + '__in':self.region_list})\
                        .filter(**{equality_rights:'Y'})

                rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                for r in rows:
                    region_id = [id for id, name in self.regions if name == r['region']][0]
                    counts.update({(r['sex'], region_id): r['n']})
        self.tabulate(ws, counts, self.male_female, self.regions, row_perc=True)

    def ws_46(self, ws):
        """
        Cols: Region, Stereotypes
        Rows: Major Topics
        """
        secondary_counts = OrderedDict()
        for region_id, region in self.regions:
            counts = Counter()
            for media_type, model in tm_sheet_models.iteritems():
                if 'stereotypes' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('stereotypes', 'topic')\
                            .filter(country_region__region=region)

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)

                    for r in rows:
                        counts.update({(TOPIC_GROUPS[r['topic']], r['stereotypes']): r['n']})
            secondary_counts[region] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=True)

    def ws_47(self, ws):
        """
        Cols: Stereotypes
        Rows: Major Topics
        """
        counts = Counter()
        for media_type, model in tm_sheet_models.iteritems():
            rows = model.objects\
                    .values('stereotypes', 'topic')\
                    .filter(country__in=self.country_list)

            rows = self.apply_weights(rows, model._meta.db_table, media_type)

            for r in rows:
                counts.update({(r['stereotypes'], TOPIC_GROUPS[r['topic']]): r['n']})

        self.tabulate(ws, counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=True)

    def ws_48(self, ws):
        """
        Cols: Sex of reporter, Stereotypes
        Rows: Major Topics
        """
        secondary_counts = OrderedDict()
        for gender_id, gender in self.male_female:
            counts = Counter()
            for media_type, model in tm_journalist_models.iteritems():
                sheet_name = model.sheet_name()
                topic = sheet_name + '__topic'
                stereotypes =  sheet_name + '__stereotypes'
                if 'stereotypes' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                    rows = model.objects\
                            .values(stereotypes, topic)\
                            .filter(sex=gender_id)\
                            .filter(**{model.sheet_name() + '__country__in':self.country_list})

                    rows = self.apply_weights(rows, model.sheet_db_table(), media_type)

                    for r in rows:
                        counts.update({(r['stereotypes'], TOPIC_GROUPS[r['topic']]): r['n']})
            secondary_counts[gender] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, MAJOR_TOPICS, row_perc=False)

    def ws_49(self, ws):
        """
        Cols: Major Topics
        Rows: Region
        :: Internet media type only
        """
        counts = Counter()
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'country_region__region')\
                .filter(country_region__region__in=self.region_list)

        rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

        for row in rows:
            region_id = [r[0] for r in self.regions if r[1] == row['region']][0]
            major_topic = TOPIC_GROUPS[row['topic']]
            counts.update({(major_topic, region_id): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, self.regions, row_perc=True)

    def ws_50(self, ws):
        """
        Cols: Major Topics
        Rows: Country
        :: Internet media type only
        :: Only stories shared on Twitter
        """
        counts = Counter()
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'country')\
                .filter(country__in=self.country_list)\
                .filter(shared_via_twitter='Y')

        rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

        for row in rows:
            major_topic = TOPIC_GROUPS[row['topic']]
            counts.update({(major_topic, self.recode_country(row['country'])): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, self.countries, row_perc=True)

    def ws_51(self, ws):
        """
        Cols: Major Topics
        Rows: Country
        :: Internet media type only
        :: Only stories shared on Facebook
        """
        counts = Counter()
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'country')\
                .filter(country__in=self.country_list)\
                .filter(shared_on_facebook='Y')

        rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

        for row in rows:
            major_topic = TOPIC_GROUPS[row['topic']]
            counts.update({(major_topic, self.recode_country(row['country'])): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, self.countries, row_perc=True)

    def ws_52(self, ws):
        """
        Cols: Major Topics
        Rows: Country
        :: Internet media type only
        :: Only stories with reference to gener equality
        """
        counts = Counter()
        model = sheet_models.get('Internet')
        rows = model.objects\
                .values('topic', 'country')\
                .filter(country__in=self.country_list)\
                .filter(equality_rights='Y')

        rows = self.apply_weights(rows, model._meta.db_table, 'Internet')

        for row in rows:
            major_topic = TOPIC_GROUPS[row['topic']]
            counts.update({(major_topic, self.recode_country(row['country'])): row['n']})

        self.tabulate(ws, counts, MAJOR_TOPICS, self.countries, row_perc=True)

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

        for major_topic, topic_ids in GROUP_TOPICS_MAP.iteritems():
            counts = Counter()
            journo_sex_field = '%s__sex' % model.journalist_field_name()
            rows = model.objects\
                .values(journo_sex_field, 'country')\
                .filter(topic__in=topic_ids)

            rows = self.apply_weights(rows, model._meta.db_table, 'Internet')
            counts.update({(r['sex'], self.recode_country(r['country'])): r['n'] for r in rows})
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.countries, row_perc=True, filter_cols=filter_cols)

    def ws_54(self, ws):
        """
        Cols: Major Topic, sex of subject
        Rows: Country
        :: Internet media type only
        """
        secondary_counts = OrderedDict()
        model = person_models.get('Internet')
        for major_topic, topic_ids in GROUP_TOPICS_MAP.iteritems():
            counts = Counter()
            country_field = '%s__country' % model.sheet_name()
            rows = model.objects\
                .values('sex', country_field)\
                .filter(**{model.sheet_name() + '__topic__in':topic_ids})

            rows = self.apply_weights(rows, model.sheet_db_table(), 'Internet')
            counts.update({(r['sex'], self.recode_country(r['country'])): r['n'] for r in rows})
            major_topic_name = [mt[1] for mt in MAJOR_TOPICS if mt[0] == int(major_topic)][0]
            secondary_counts[major_topic_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.countries, row_perc=True)

    def ws_55(self, ws):
        """
        Cols: Occupation
        Rows: Country
        :: Show all countries
        :: Only female subjects
        :: Internet media type only
        """
        counts = Counter()
        model = person_models.get('Internet')
        country_field = '%s__country' % model.sheet_name()

        rows = model.objects\
                .values(country_field, 'occupation')\
                .filter(sex=1)

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        counts.update({(r['occupation'], self.recode_country(r['country'])): r['n'] for r in rows})
        self.tabulate(ws, counts, OCCUPATION, self.countries, row_perc=True)

    def ws_56(self, ws):
        """
        Cols: Function
        Rows: Country
        :: Show all countries
        :: Internet media type only
        """
        counts = Counter()
        model = person_models.get('Internet')
        country_field = '%s__country' % model.sheet_name()
        rows = model.objects\
                .values(country_field, 'function')\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        counts.update({(r['function'], self.recode_country(r['country'])): r['n'] for r in rows})
        self.tabulate(ws, counts, FUNCTION, self.countries, row_perc=True)

    def ws_57(self, ws):
        """
        Cols: Sex of subject
        Rows: Country, Family role
        :: Show all countries
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        counts = Counter()
        model = person_models.get('Internet')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'family_role')\
                    .filter(**{model.sheet_name() + '__country':code})

            rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")

            counts = {(row['sex'], row['family_role']): row['n'] for row in rows}
            # If only captured countries should be displayed use
            # if counts.keys():
            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, YESNO, row_perc=True, write_col_headings=False, r=r)
            r += len(YESNO)

    def ws_58(self, ws):
        """
        Cols: Sex of subject
        Rows: Country, is photographed
        :: Show all countries
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        counts = Counter()
        model = person_models.get('Internet')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'is_photograph')\
                    .filter(**{model.sheet_name() + '__country':code})

            rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
            counts = {(row['sex'], row['is_photograph']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, IS_PHOTOGRAPH, row_perc=True, write_col_headings=False, r=r)
            r += len(IS_PHOTOGRAPH)

    def ws_59(self, ws):
        """
        Cols: Sex of reporter
        Rows: Sex of subject
        :: Internet media only
        """
        counts = Counter()
        model = person_models.get('Internet')
        sheet_name = model.sheet_name()
        journo_name = model._meta.get_field(model.sheet_name()).rel.to.journalist_field_name()
        journo_sex = sheet_name + '__' + journo_name + '__sex'

        rows = model.objects\
                .extra(select={"subject_sex": model._meta.db_table + ".sex"})\
                .values(journo_sex, 'subject_sex')\
                .filter(**{model.sheet_name() + '__country__in':self.country_list})\
                .annotate(n=Count('id'))

        rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
        counts.update({(r['sex'], r['subject_sex']): r['n'] for r in rows})
        counts['col_title_def'] = 'Sex of reporter'

        self.tabulate(ws, counts, GENDER, GENDER, row_perc=False)

    def ws_60(self, ws):
        """
        Cols: Sex of subject
        Rows: Country, age
        :: Show all countries
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        counts = Counter()
        model = person_models.get('Internet')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'age')\
                    .filter(**{model.sheet_name() + '__country':code})

            rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
            counts = {(row['sex'], row['age']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, AGES, row_perc=True, write_col_headings=False, r=r)
            r += len(AGES)

    def ws_61(self, ws):
        """
        Cols: Sex of subject
        Rows: Country, is_quoted
        :: Show all countries
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        counts = Counter()
        model = person_models.get('Internet')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'is_quoted')\
                    .filter(**{model.sheet_name() + '__country':code})

            rows = self.apply_weights(rows, model.sheet_db_table(), "Internet")
            counts = {(row['sex'], row['is_quoted']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, YESNO, row_perc=True, write_col_headings=False, r=r)
            r += len(YESNO)

    def ws_62(self, ws):
        """
        Cols: Topic
        Rows: Country, equality raised
        :: Show all countries
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, TOPICS)

        counts = Counter()
        model = sheet_models.get('Internet')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'equality_rights')\
                    .filter(country=code)

            rows = self.apply_weights(rows, model._meta.db_table, "Internet")
            counts = {(row['topic'], row['equality_rights']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, YESNO, row_perc=True, write_col_headings=False, r=r)
            r += len(YESNO)

    def ws_63(self, ws):
        """
        Cols: Topic
        Rows: Country, stereotypes challenged
        :: Show all countries
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, TOPICS)

        counts = Counter()
        model = sheet_models.get('Internet')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'stereotypes')\
                    .filter(country=code)

            rows = self.apply_weights(rows, model._meta.db_table, "Internet")
            counts = {(row['topic'], row['stereotypes']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, AGREE_DISAGREE, row_perc=True, write_col_headings=False, r=r)
            r += len(AGREE_DISAGREE)

    def ws_64(self, ws):
        """
        Cols: Topic
        Rows: Country, about women
        :: Show all countries
        :: Internet media type only
        """
        r = 6
        self.write_col_headings(ws, TOPICS)

        counts = Counter()
        model = sheet_models.get('Internet')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'about_women')\
                    .filter(country=code)

            rows = self.apply_weights(rows, model._meta.db_table, "Internet")
            counts = {(row['topic'], row['about_women']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, YESNO, row_perc=True, write_col_headings=False, r=r)
            r += len(YESNO)

    def ws_65(self, ws):
        """
        Cols: Topic
        Rows: Country, tweet or retweet
        :: Show all countries
        :: Twitter media type only
        """
        r = 6
        self.write_col_headings(ws, TOPICS)

        counts = Counter()
        model = sheet_models.get('Twitter')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'retweet')\
                    .filter(country=code)

            rows = self.apply_weights(rows, model._meta.db_table, "Twitter")
            counts = {(row['topic'], row['retweet']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, RETWEET, row_perc=False, write_col_headings=False, r=r)
            r += len(RETWEET)

    def ws_66(self, ws):
        """
        Cols: Topic
        Rows: Country, sex of news subject
        :: Show all countries
        :: Twitter media type only
        """
        r = 6
        self.write_col_headings(ws, TOPICS)

        counts = Counter()
        model = person_models.get('Twitter')
        topic_field = '%s__topic' % model.sheet_name()
        for code, country in self.countries:
            rows = model.objects\
                    .values(topic_field, 'sex')\
                    .filter(**{model.sheet_name() + '__country':code})

            rows = self.apply_weights(rows, model.sheet_db_table(), "Twitter")
            counts.update({(row['topic'], row['sex']): row['n'] for row in rows})

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, GENDER, row_perc=True, write_col_headings=False, r=r)
            r += len(GENDER)

    def ws_67(self, ws):
        """
        Cols: Topic
        Rows: Country
        :: Only female journalists
        :: Show all countries
        :: Twitter media type only
        """
        counts = Counter()
        model = sheet_models.get('Twitter')
        rows = model.objects\
                .values('topic', 'country')\
                .filter(**{model.journalist_field_name() + '__sex':1})

        rows = self.apply_weights(rows, model._meta.db_table, "Twitter")
        counts.update({(row['topic'], self.recode_country(row['country'])): row['n'] for row in rows})

        self.tabulate(ws, counts, TOPICS, self.countries, row_perc=True)

    def ws_68(self, ws):
        """
        Cols: Topic
        Rows: Country, about women
        :: Show all countries
        :: Twitter media type only
        """
        r = 6
        self.write_col_headings(ws, TOPICS)

        counts = Counter()
        model = sheet_models.get('Twitter')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'about_women')\
                    .filter(country=code)

            rows = self.apply_weights(rows, model._meta.db_table, "Twitter")
            counts = {(row['topic'], row['about_women']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, YESNO, row_perc=False, write_col_headings=False, r=r)
            r += len(YESNO)

    def ws_68b(self, ws):
        """
        Cols: Topic
        Rows: Country, stereotypes
        :: Show all countries
        :: Twitter media type only
        """
        r = 6
        self.write_col_headings(ws, TOPICS)

        counts = Counter()
        model = sheet_models.get('Twitter')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'stereotypes')\
                    .filter(country=code)

            rows = self.apply_weights(rows, model._meta.db_table, "Twitter")
            counts = {(row['topic'], row['stereotypes']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, AGREE_DISAGREE, row_perc=True, write_col_headings=False, r=r)
            r += len(AGREE_DISAGREE)

    def ws_72(self, ws):
        """
        Cols: Focus Topic, Media
        Rows: Country
        Focus: female reporters
        """
        # TODO: these values should be %age total of media in country/region

        secondary_counts = OrderedDict()
        for topic_id, topic in FOCUS_TOPICS.iteritems():
            actual_topic_ids = [k for k, v in FOCUS_TOPIC_MAP.iteritems() if v == topic_id]
            counts = Counter()
            secondary_counts[topic] = counts

            for media_type, model in sheet_models.iteritems():
                journo_name = model.journalist_field_name()
                media_id = [m[0] for m in MEDIA_TYPES if m[1] == media_type][0]

                rows = model.objects\
                    .values('country')\
                    .filter(**{journo_name + '__sex': self.female[0][0]})\
                    .filter(topic__in=actual_topic_ids)

                rows = self.apply_weights(rows, model._meta.db_table, media_type)
                counts.update({(media_id, self.recode_country(r['country'])): r['n'] for r in rows})

        self.tabulate_secondary_cols(ws, secondary_counts, MEDIA_TYPES, self.countries, show_N=True)

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
            for topic_id, topic in FOCUS_TOPICS.iteritems():
                counts = Counter()
                secondary_counts[topic] = counts
                actual_topic_ids = [k for k, v in FOCUS_TOPIC_MAP.iteritems() if v == topic_id]

                for media_type, model in models.iteritems():
                    rows = model.objects\
                        .values('country', 'about_women')\
                        .filter(country__in=self.country_list)\
                        .filter(topic__in=actual_topic_ids)

                    rows = self.apply_weights(rows, model._meta.db_table, media_type)
                    counts.update({(r['about_women'], self.recode_country(r['country'])): r['n'] for r in rows})

            self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.countries, row_perc=True, c=c, r=7)
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
            for topic_id, topic in TOPICS:
                counts = Counter()
                secondary_counts[topic] = counts
                for media_type, model in models.iteritems():
                    if 'stereotypes' in model._meta.get_all_field_names():
                        rows = model.objects\
                            .values('stereotypes', 'country')\
                            .filter(topic=topic_id)

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
            for topic_id, topic in TOPICS:
                counts = Counter()
                for media_type, model in models.iteritems():
                    if 'equality_rights' in model._meta.get_all_field_names():
                        rows = model.objects\
                            .values('equality_rights', 'country')\
                            .filter(topic=topic_id)

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
            for topic_id, topic in TOPICS:
                counts = Counter()
                for media_type, model in models.iteritems():
                    if 'victim_of' in model._meta.get_all_field_names():
                        country_field = '%s__country' % model.sheet_name()
                        rows = model.objects\
                            .values('victim_of', country_field)\
                            .filter(**{model.sheet_name() + '__topic':topic_id})

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
            for topic_id, topic in TOPICS:
                counts = Counter()
                for media_type, model in models.iteritems():
                    if 'survivor_of' in model._meta.get_all_field_names():
                        country_field = '%s__country' % model.sheet_name()
                        rows = model.objects\
                            .values('survivor_of', country_field)\
                            .filter(**{model.sheet_name() + '__topic':topic_id})

                        rows = self.apply_weights(rows, model.sheet_db_table(), media_type)
                        counts.update({(r['survivor_of'], self.recode_country(r['country'])): r['n'] for r in rows})

                    secondary_counts[topic] = counts

            self.tabulate_secondary_cols(ws, secondary_counts, SURVIVOR_OF, self.countries, row_perc=True, c=c, r=8)
            c = ws.dim_colmax + 2

    # -------------------------------------------------------------------------------
    # Helper functions
    #
    def write_headers(self, ws, title, description):
        """
        Write the headers to the worksheet
        """
        ws.write(0, 0, title, self.heading)
        ws.write(1, 0, description, self.heading)
        ws.write(3, 2, self.gmmp_year, self.heading)

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

    def tabulate_secondary_cols(self, ws, secondary_counts, cols, rows, row_perc=False, write_row_headings=True, filter_cols=None, c=1, r=7, show_N=False):
        """
        :param ws: worksheet to write to
        :param secondary_counts: dict in following format:
            {'Primary column heading': Count object, ...}
        :param list cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param list rows: list of `(row_id, row_heading)` tuples of row ids and titles
        :param bool row_perc: should percentages by calculated by row instead of column (default: False)
        """

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
        sec_cols = len(cols)
        if show_N:
            sec_cols *= 2
        if row_perc:
            sec_cols += 1

        for field, counts in secondary_counts.iteritems():
            ws.merge_range(r-3, c, r-3, c+sec_cols-1, clean_title(field), self.sec_col_heading)
            self.tabulate(ws, counts, cols, rows, row_perc=row_perc, write_row_headings=False, filter_cols=filter_cols, r=r, c=c, show_N=show_N)
            c += sec_cols

    def tabulate(self, ws, counts, cols, rows, row_perc=False,
                 write_row_headings=True, write_col_headings=True,
                 filter_cols=None, c=1, r=6, show_N=False):
        """ Emit a table.

        :param ws: worksheet to write to
        :param dict counts: dict from `(col_id, row_id)` tuples to count for that combination.
        :param list cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param list rows: list of `(row_id, row_heading)` tuples of row ids and titles
        :param bool row_perc: should percentages by calculated by row instead of column (default: False)
        :param write_row_headings: Should we write the row headings. False if already written.
        :param write_col_headings: Should we write the col headings. False if already written.
        :param filter_cols: If not None, display only passed subset of columns e.g. only female
        :param r, c: initial position where cursor should start writing to
        """
        if row_perc:
            # Calc percentage by row
            row_totals = {}
            for row_id, row_heading in rows:
                row_totals[row_id] = sum(counts.get((col_id, row_id), 0) for col_id, _ in cols)  # noqa

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

        if 'col_title_def' in counts and write_col_headings:
            # write definition of column headings
            ws.write(r-2, c-1, counts['col_title_def'], self.col_heading_def)
            counts.pop('col_title_def')

        # values, written column by column
        if show_N:
            for col_id, col_heading in cols:
                # column title
                if write_col_headings:
                    # else already written
                    ws.merge_range(r-2, c, r-2, c+1, clean_title(col_heading), self.col_heading)
                    ws.write(r-1, c, "N", self.label)
                    ws.write(r-1, c+1, "%", self.label)

                if not row_perc:
                    # column totals
                    # Confirm: Perc of col total or matrix total?
                    # total = sum(counts.itervalues())
                    total = sum(counts.get((col_id, row_id), 0) for row_id, _ in rows)

                # values for this column
                # col_total_n = 0
                col_total_perc = 0
                for i, row in enumerate(rows):
                    row_id, row_title = row

                    if row_perc:
                        # row totals
                        total = row_totals[row_id]

                    n = counts.get((col_id, row_id), 0)
                    perc = p(n, total)

                    ws.write(r+i, c, n, self.N)
                    ws.write(r+i, c+1, perc, self.P)

                    # col_total_n += n
                    col_total_perc += perc

                if row_perc:
                    # col_total_n = col_total_n / len(rows)
                    col_total_perc = col_total_perc / len (rows)

                # ws.write(r + i + 1, c, col_total_n, self.N)
                ws.write(r+i+1, c+1, col_total_perc, self.P)
                c += 2

        else:
            # only write %'s
            for col_id, col_heading in cols:
                # column title
                if write_col_headings:
                    # else already written
                    ws.write(r-2, c, clean_title(col_heading), self.col_heading)
                    ws.write(r-1, c, "%", self.label)

                total = sum(counts.get((col_id, row_id), 0) for row_id, _ in rows)

                # values for this column
                col_total = 0
                for i, row in enumerate(rows):
                    row_id, row_title = row

                    if row_perc:
                        # row totals
                        total = row_totals[row_id]

                    n = counts.get((col_id, row_id), 0)
                    perc = p(n, total)
                    ws.write(r+i, c, perc, self.P)
                    col_total += perc
                if row_perc:
                    col_total = col_total / len(rows)
                ws.write(r+i+1, c, col_total, self.P)

                c += 1

            if row_perc:
                # Write the row totals
                for i, row in enumerate(rows):
                    row_id, row_title = row
                    ws.write(r+i, c, row_totals[row_id], self.N)
