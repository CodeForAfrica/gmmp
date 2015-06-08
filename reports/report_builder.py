# Python
import StringIO
from collections import Counter, OrderedDict

# Django
from django.core import urlresolvers
from django_countries import countries
from django.db.models import Count, FieldDoesNotExist
from django.contrib.sites.shortcuts import get_current_site

# 3rd Party
import xlsxwriter

# Project
from forms.models import (
    NewspaperSheet, NewspaperPerson, TelevisionJournalist,
    person_models, sheet_models, journalist_models)
from forms.modelutils import (TOPICS, GENDER, SPACE, OCCUPATION, FUNCTION, SCOPE,
    YESNO, AGES, SOURCE, VICTIM_OF, SURVIVOR_OF, IS_PHOTOGRAPH, AGREE_DISAGREE,
    RETWEET, TV_ROLE, MEDIA_TYPES,
    CountryRegion)
from report_details import WS_INFO, REGION_COUNTRY_MAP, MAJOR_TOPICS, TOPIC_GROUPS


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
    return text[text.find(')')+1:].lstrip()

class XLSXDataExportBuilder():
    def __init__(self, request):
        self.domain = "http://%s" % get_current_site(request).domain

        self.sheet_exclude_fields = ['monitor', 'url_and_multimedia', 'time_accessed', 'country_region']
        self.person_exclude_fields = []
        self.journalist_exclude_fields =[]

        self.sheet_fields_with_id = ['topic', 'scope', 'person_secondary', 'inequality_women', 'stereotypes']
        self.person_fields_with_id = ['sex', 'age', 'occupation', 'function', 'survivor_of', 'victim_of']
        self.journalist_fields_with_id = ['sex', 'age']


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

        fields = [field for field in model._meta.fields if not field.name in self.sheet_exclude_fields]
        ws, col = self.write_ws_titles(ws, row, col, fields, self.sheet_fields_with_id)

        row += 1
        col = 0

        for y, obj in enumerate(obj_list):
            col = 0
            ws, col = self.write_sheet_row(obj, ws, row+y, col, fields, self.sheet_fields_with_id)

    def create_person_export(self, model, wb):
        ws = wb.add_worksheet(model._meta.object_name)
        obj_list = model.objects.all().prefetch_related(model.sheet_name())
        row, col = 0, 0

        fields = [field for field in model._meta.fields if not field.name in self.person_exclude_fields]
        ws, col = self.write_ws_titles(ws, row, col, fields, self.person_fields_with_id)

        sheet_model = model._meta.get_field(model.sheet_name()).rel.to

        sheet_fields = [field for field in sheet_model._meta.fields if not field.name in self.sheet_exclude_fields]
        ws, col = self.write_ws_titles(ws, row, col, sheet_fields, self.sheet_fields_with_id, append_sheet=True)

        row += 1

        for y, obj in enumerate(obj_list):
            col = 0
            ws, col = self.write_person_row(obj, ws, row+y, col, fields, self.person_fields_with_id)
            col += 1
            sheet_obj = getattr(obj, model.sheet_name())
            ws, col = self.write_sheet_row(sheet_obj, ws, row+y, col, sheet_fields, self.sheet_fields_with_id)

    def create_journalist_export(self, model, wb):
        ws = wb.add_worksheet(model._meta.object_name)
        obj_list = model.objects.all().prefetch_related(model.sheet_name())
        row, col = 0, 0
        fields = [field for field in model._meta.fields if not field.name in self.journalist_exclude_fields]

        ws, col = self.write_ws_titles(ws, row, col, fields, self.journalist_fields_with_id)

        sheet_model = model._meta.get_field(model.sheet_name()).rel.to

        sheet_fields = [field for field in sheet_model._meta.fields if not field.name in self.sheet_exclude_fields]
        ws, col = self.write_ws_titles(ws, row, col, sheet_fields, self.sheet_fields_with_id, append_sheet=True)

        row += 1
        col = 0

        for y, obj in enumerate(obj_list):
            col = 0
            ws, col = self.write_journalist_row(obj, ws, row+y, col, fields, self.journalist_fields_with_id)
            col += 1
            sheet_obj = getattr(obj, model.sheet_name())
            ws, col = self.write_sheet_row(sheet_obj, ws, row+y, col, sheet_fields, self.sheet_fields_with_id)

    def write_ws_titles(self, ws, row, col, fields, fields_with_id, append_sheet=False):
        """
        Writes the column titles to the worksheet

        :param ws: Reference to the current worksheet
        :param row, col: y,x postion of the cursor
        :param fields: list of fields of the model which need to be written to the sheet
        :param fields_with_id: fields which need to be written over two columns: id + name
        :param append_sheet: Boolean specifying whether the related sheet object
                             needs to be appended to the row.
        """
        if not append_sheet:
            for field in fields:
                ws.write(row, col, unicode(field.name))
                col += 1
                if field.name in fields_with_id:
                    ws.write(row, col, unicode(field.name+"_id"))
                    col += 1
            ws.write(row, col, unicode('edit_url'))
            col += 1
        else:
            for field in fields:
                ws.write(row, col, unicode("sheet_" + field.name))
                col += 1
                if field.name in fields_with_id:
                    ws.write(row, col, unicode("sheet_" + field.name + "_id"))
                    col += 1
            ws.write(row, col, unicode('sheet_edit_url'))
            col += 1
        return ws, col

    def write_sheet_row(self, obj, ws, row, col, fields, fields_with_id):
        """
        Writes a row of data of Sheet models to the worksheet

        :param obj: Reference to the model instance which is being written to the sheet
        :param ws: Reference to the current worksheet
        :param row, col: y,x postion of the cursor
        :param fields: list of fields of the model which need to be written to the sheet
        :param fields_with_id: fields which need to be written over two columns: id + name
        """
        for field in fields:
            # Certain fields are 1-indexed
            if field.name == 'country':
                ws.write(row, col, getattr(obj, field.name).code)
            elif field.name == 'topic':
                ws.write(row, col, unicode(TOPICS[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, TOPICS[getattr(obj, field.name)-1][0])
            elif field.name == 'scope':
                ws.write(row, col, unicode(SCOPE[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, SCOPE[getattr(obj, field.name)-1][0])
            elif field.name == 'person_secondary':
                ws.write(row, col, unicode(SOURCE[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, SOURCE[getattr(obj, field.name)][0])
            elif field.name == 'inequality_women':
                ws.write(row, col, unicode(AGREE_DISAGREE[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, AGREE_DISAGREE[getattr(obj, field.name)-1][0])
            elif field.name == 'stereotypes':
                ws.write(row, col, unicode(AGREE_DISAGREE[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, AGREE_DISAGREE[getattr(obj, field.name)-1][0])
            elif field.name == 'space':
                ws.write(row, col, unicode(SPACE[getattr(obj, field.name)-1][1]))
            elif field.name == 'retweet':
                ws.write(row, col, unicode(RETWEET[getattr(obj, field.name)-1][1]))
            else:
                try:
                    ws.write(row, col, unicode(getattr(obj, field.name)))
                    if field.name in fields_with_id:
                        col += 1
                except UnicodeEncodeError:
                    ws.write(row, col, unicode(getattr(obj, field.name).encode('ascii', 'replace')))
            col += 1
        change_url = urlresolvers.reverse(
            'admin:%s_%s_change' % (
                obj._meta.app_label,
                obj._meta.model_name),
            args=(obj.id,))
        ws.write_url(row, col, "%s%s" % (self.domain, change_url))

        return ws, col

    def write_person_row(self, obj, ws, row, col, fields, fields_with_id):
        """
        Writes a row of data of Person models to the worksheet

        :param obj: Reference to the model instance which is being written to the sheet
        :param ws: Reference to the current worksheet
        :param row, col: y,x postion of the cursor
        :param fields: list of fields of the model which need to be written to the sheet
        :param fields_with_id: fields which need to be written over two columns: id + name
        """
        for field in fields:
            # Certain fields are 1-indexed
            if field.name == 'sex':
                ws.write(row, col, unicode(GENDER[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, GENDER[getattr(obj, field.name)-1][0])
            elif field.name == 'age':
                ws.write(row, col, unicode(AGES[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, AGES[getattr(obj, field.name)][0])
            elif field.name == 'occupation':
                ws.write(row, col, unicode(OCCUPATION[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, OCCUPATION[getattr(obj, field.name)][0])
            elif field.name == 'function':
                ws.write(row, col, unicode(FUNCTION[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, FUNCTION[getattr(obj, field.name)][0])
            elif field.name == 'victim_of' and not getattr(obj, field.name) == None:
                ws.write(row, col, unicode(VICTIM_OF[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, VICTIM_OF[getattr(obj, field.name)][0])
            elif field.name == 'survivor_of' and not getattr(obj, field.name) == None:
                ws.write(row, col, unicode(SURVIVOR_OF[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, SURVIVOR_OF[getattr(obj, field.name)][0])
            elif field.name == 'is_photograph':
                ws.write(row, col, unicode(IS_PHOTOGRAPH[getattr(obj, field.name)-1][1]))
            elif field.name == 'space':
                ws.write(row, col, unicode(SPACE[getattr(obj, field.name)-1][1]))
            elif field.name == 'retweet':
                ws.write(row, col, unicode(RETWEET[getattr(obj, field.name)-1][1]))
            elif field.name == obj.sheet_name():
                ws.write(row, col, getattr(obj, field.name).id)
                # Get the parent model and id for building the edit link
                parent_model = field.related.parent_model
                parent_id = getattr(obj, field.name).id
            else:
                try:
                    ws.write(row,col, unicode(getattr(obj, field.name)))
                    if field.name in self.person_fields_with_id:
                        col += 1
                except UnicodeEncodeError:
                    ws.write(row,col, unicode(getattr(obj, field.name).encode('ascii', 'replace')))
            col += 1
        # Write link to end of row
        change_url = urlresolvers.reverse(
            'admin:%s_%s_change' % (
                parent_model._meta.app_label,
                parent_model._meta.model_name),
            args=(parent_id,))
        ws.write_url(row, col, "%s%s" % (self.domain, change_url))

        return ws, col

    def write_journalist_row(self, obj, ws, row, col, fields, fields_with_id):
        """
        Writes a row of data of Journalist models to the worksheet

        :param obj: Reference to the model instance which is being written to the sheet_fields_with_id
        :param ws: Reference to the current worksheet
        :param row, col: y,x postion of the cursor
        :param fields: list of fields of the model which need to be written to the sheet_fields_with_id
        :param fields_with_id: fields which need to be written over two columns: id + name
        """
        for field in fields:
            if field.name == 'sex':
                ws.write(row, col, unicode(GENDER[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, GENDER[getattr(obj, field.name)-1][0])
            elif field.name == 'age' and not getattr(obj, field.name) == None:
                ws.write(row, col, unicode(AGES[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, AGES[getattr(obj, field.name)][0])
            elif field.name == obj.sheet_name():
                ws.write(row, col, getattr(obj, field.name).id)
                # Get the parent model and id for building the edit link
                parent_model = field.related.parent_model
                parent_id = getattr(obj, field.name).id
            else:
                try:
                    ws.write(row,col, unicode(getattr(obj, field.name)))
                    if field.name in fields_with_id:
                        col += 1
                except UnicodeEncodeError:
                    ws.write(row,col, unicode(getattr(obj, field.name).encode('ascii', 'replace')))
            col += 1
        # Write link to end of row
        change_url = urlresolvers.reverse(
            'admin:%s_%s_change' % (
                parent_model._meta.app_label,
                parent_model._meta.model_name),
            args=(parent_id,))
        ws.write_url(row, col, "%s%s" % (self.domain, change_url))

        return ws, col


class XLSXReportBuilder:
    def __init__(self, form):
        from reports.views import CountryForm, RegionForm
        self.form = form
        if isinstance(form, CountryForm):
            self.countries = form.filter_countries()
            self.regions = get_country_region(form.cleaned_data['country'])
        elif isinstance(form, RegionForm):
            region = [name for i, name in form.REGIONS if str(i) == form.cleaned_data['region']][0]
            self.countries = get_region_countries(region)
            self.regions = [(0, region)]
        else:
            self.countries = get_countries()
            self.regions = get_regions()

        self.country_list = [code for code, name in self.countries]
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

        # Use the following for specifying which reports to create durin dev
        test_functions = ['ws_04']

        sheet_info = OrderedDict(sorted(WS_INFO.items(), key=lambda t: t[0]))
        for function in test_functions:
            ws = workbook.add_worksheet(sheet_info[function]['name'])
            self.write_headers(ws, sheet_info[function]['title'], sheet_info[function]['desc'])
            getattr(self, function)(ws)

        # -------------------------------------------------------------------

        # To ensure ordered worksheets
        # sheet_info = OrderedDict(sorted(WS_INFO.items(), key=lambda t: t[0]))

        # for ws_num, ws_info in sheet_info.iteritems():
        #     ws = workbook.add_worksheet(ws_info['name'])
        #     self.write_headers(ws, ws_info['title'], ws_info['desc'])
        #     getattr(self, ws_num)(ws)

        workbook.close()
        output.seek(0)

        return output.read()


    def ws_01(self, ws):
        """
        Cols: Media Type
        Rows: Region
        """
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
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

        self.tabulate(ws, counts, MEDIA_TYPES, self.regions, row_perc=True)


    def ws_02(self, ws):
        """
        Cols: Media Type
        Rows: Country
        """
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            rows = model.objects\
                    .values('country')\
                    .annotate(n=Count('country'))

            for row in rows:
                if row['country'] is not None:
                    # Get media id's to assign to counts
                    media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                    counts.update({(media_id, row['country']): row['n']})

        self.tabulate(ws, counts, MEDIA_TYPES, self.countries, row_perc=True)

    def ws_04(self, ws):
        """
        Cols: Region, Media type
        Rows: News Topic
        """
        secondary_counts = OrderedDict()
        for region_id, region in self.regions:
            counts = Counter()
            for media_type, model in sheet_models.iteritems():
                rows = model.objects\
                        .values('topic')\
                        .filter(country__in=self.country_list)\
                        .annotate(n=Count('id'))

                for row in rows:
                    # Get media id's to assign to counts
                    media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                    major_topic = [k for k, v in TOPIC_GROUPS.iteritems() if row['topic'] in v][0]
                    counts.update({(media_id, major_topic): row['n']})
            secondary_counts[region] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, MEDIA_TYPES, MAJOR_TOPICS, row_perc=False, sec_cols=10)

    def ws_05(self, ws):
        """
        Cols: Subject sex
        Rows: Topic
        """
        counts = Counter()
        for model in person_models.itervalues():
            topic_field = '%s__topic' % model.sheet_name()

            rows = model.objects\
                .values('sex', topic_field)\
                .filter(**{model.sheet_name() + '__country__in': self.countries})\
                .annotate(n=Count('id'))
            counts.update({(r['sex'], r[topic_field]): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, TOPICS, row_perc=True)

    def ws_06(self, ws):
        """
        Cols: Topic, victim_of
        Rows: Country
        """
        secondary_counts = OrderedDict()
        for region_id, region in self.regions:
            counts = Counter()
            for model in person_models.itervalues():
                topic_field = '%s__topic' % model.sheet_name()
                rows = model.objects\
                    .values('sex', topic_field)\
                    .filter(**{model.sheet_name() + '__country_region__region':region})\
                    .annotate(n=Count('id'))
                counts.update({(r['sex'], r[topic_field]): r['n'] for r in rows})
            secondary_counts[region] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, TOPICS, row_perc=True, sec_cols=8)

    def ws_07(self, ws):
        """
        Cols: Media Type
        Rows: Sex
        """
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            sex = '%s__sex' % model.person_field_name()
            rows = model.objects\
                    .values(sex)\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))

            for row in rows:
                # Get media id's to assign to counts
                media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                counts.update({(media_id, row[sex]): row['n']})

        self.tabulate(ws, counts, MEDIA_TYPES, GENDER, row_perc=True)

    def ws_08(self, ws):
        """
        Cols: Sex
        Rows: Scope
        """
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

    def ws_09(self, ws):
        """
        Cols: Sex
        Rows: Topic
        """
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            sex = '%s__sex' % model.person_field_name()
            rows = model.objects\
                    .values(sex, 'topic')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))
            counts.update({(r[sex], r['topic']): r['n'] for r in rows if r[sex] is not None})

        self.tabulate(ws, counts, GENDER, TOPICS, row_perc=True)

    def ws_10(self, ws):
        """
        Cols: Space
        Rows: Topic
        """
        # Calculate row values for column
        counts = Counter()
        rows = NewspaperSheet.objects\
                .values('space', 'topic')\
                .filter(country__in=self.countries)\
                .annotate(n=Count('id'))
        counts.update({(r['space'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, SPACE, TOPICS, row_perc=True)

    def ws_11(self, ws):
        """
        Cols: Equality Rights
        Rows: Topic
        """
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            if 'equality_rights' in model._meta.get_all_field_names():
                rows = model.objects\
                    .values('equality_rights', 'topic')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))
                counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, YESNO, TOPICS, row_perc=True)

    def ws_12(self, ws):
        """
        Cols: Region, Equality Rights
        Rows: Topics
        """
        secondary_counts = OrderedDict()
        for region_id, region_name in get_regions():
            counts = Counter()
            for media_type, model in sheet_models.iteritems():
                # Some models has no equality rights field
                if 'equality_rights' in model._meta.get_all_field_names():
                    rows = model.objects\
                        .values('equality_rights', 'topic', 'country_region__region')\
                        .filter(country_region__region=region_name)\
                        .annotate(n=Count('id'))
                    counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
            secondary_counts[region_name] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, TOPICS, row_perc=True, sec_cols=4)

    def ws_13(self, ws):
        """
        Cols: Journalist Sex
        Rows: Topics
        """
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            sex = '%s__sex' % model.journalist_field_name()
            rows = model.objects\
                    .values(sex, 'topic')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))
            counts.update({(r[sex], r['topic']): r['n'] for r in rows if r[sex] is not None})

        self.tabulate(ws, counts, GENDER, TOPICS, row_perc=True)

    def ws_14(self, ws):
        """
        Cols: Sex
        Rows: Occupation
        """
        counts = Counter()
        for model in person_models.itervalues():
            # some Person models don't have an occupation field
            if 'occupation' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'occupation')\
                        .filter(**{model.sheet_name() + '__country__in': self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, OCCUPATION, row_perc=True)

    def ws_15(self, ws):
        """
        Cols: Sex
        Rows: Function
        """
        counts = Counter()

        for model in person_models.itervalues():
            # some Person models don't have a function field
            if 'function' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'function')\
                        .filter(**{model.sheet_name() + '__country__in': self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['function']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, FUNCTION, row_perc=True)

    def ws_16(self, ws):
        """
        Cols: Occupation, Sex
        Rows: Function
        """
        secondary_counts = OrderedDict()
        for occ_id, occupation in OCCUPATION:
            counts = Counter()
            for model in person_models.itervalues():
                if 'function' in model._meta.get_all_field_names() and 'occupation' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('sex', 'function')\
                            .filter(**{model.sheet_name() + '__country__in':self.countries})\
                            .filter(occupation=occ_id)\
                            .annotate(n=Count('id'))
                    counts.update({(r['sex'], r['function']): r['n'] for r in rows})
            secondary_counts[occupation] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, FUNCTION, row_perc=True, sec_cols=8)

    def ws_17(self, ws):
        """
        Cols: Age, Sex
        Rows: Function
        """
        secondary_counts = OrderedDict()
        for age_id, age in AGES:
            counts = Counter()
            for model in person_models.itervalues():
                if 'function' in model._meta.get_all_field_names() and 'age' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('sex', 'function')\
                            .filter(**{model.sheet_name() + '__country__in':self.countries})\
                            .filter(age=age_id)\
                            .annotate(n=Count('id'))
                    counts.update({(r['sex'], r['function']): r['n'] for r in rows})
            secondary_counts[age] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, FUNCTION, row_perc=True, sec_cols=8)

    def ws_18(self, ws):
        """
        Cols: Sex
        Rows: Age
        :: Only for print
        """
        counts = Counter()
        rows = NewspaperPerson.objects\
                .values('sex', 'age')\
                .filter(newspaper_sheet__country__in=self.countries)\
                .annotate(n=Count('id'))
        counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, AGES, row_perc=False)

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
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, AGES, row_perc=False)

    def ws_20(self, ws):
        """
        Cols: Function, Sex
        Rows: Occupation
        """
        secondary_counts = OrderedDict()

        functions_count = Counter()
        # Get top 5 functions
        for model in person_models.itervalues():
            if 'function' in model._meta.get_all_field_names() and 'occupation' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('function')\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .annotate(n=Count('id'))
                functions_count.update({(r['function']): r['n'] for r in rows})

        top_5_function_ids = [id for id, count in sorted(functions_count.items(), key=lambda x: -x[1])[:5]]
        top_5_functions = [(id, func) for id, func in FUNCTION if id in top_5_function_ids]

        for func_id, function in top_5_functions:
            counts = Counter()
            for model in person_models.itervalues():
                if 'function' in model._meta.get_all_field_names() and 'occupation' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('sex', 'occupation')\
                            .filter(**{model.sheet_name() + '__country__in':self.countries})\
                            .filter(function=func_id)\
                            .annotate(n=Count('id'))
                    counts.update({(r['sex'], r['occupation']): r['n'] for r in rows})
            secondary_counts[function] = counts
        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, OCCUPATION, row_perc=True, sec_cols=8)

    def ws_21(self, ws):
        """
        Cols: Sex
        Rows: Victim type
        """
        counts = Counter()
        for model in person_models.itervalues():
            if 'victim_of' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'victim_of')\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .exclude(victim_of=None)\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['victim_of']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, VICTIM_OF, row_perc=True)

    def ws_23(self, ws):
        """
        Cols: Sex
        Rows: Survivor type
        """
        counts = Counter()
        for model in person_models.itervalues():
            if 'survivor_of' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'survivor_of')\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .exclude(survivor_of=None)\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['survivor_of']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, SURVIVOR_OF, row_perc=True)

    def ws_24(self, ws):
        """
        Cols: Sex
        Rows: Family Role
        """
        counts = Counter()
        for model in person_models.itervalues():
            if 'family_role' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'family_role')\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['family_role']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, YESNO, row_perc=True)

    def ws_25(self, ws):
        """
        Cols: Sex of journalist, Sex of person
        Rows: Family Role
        """
        secondary_counts = OrderedDict()
        male_female = {(id, name) for id, name in GENDER if id in [1,2]}
        for sex_id, sex in male_female:
            counts = Counter()
            for model in person_models.itervalues():
                if 'family_role' in model._meta.get_all_field_names():
                    sheet_name = model.sheet_name()
                    journo_name = model._meta.get_field(model.sheet_name()).rel.to.journalist_field_name()
                    rows = model.objects\
                            .values('sex', 'family_role')\
                            .filter(**{model.sheet_name() + '__country__in':self.countries})\
                            .filter(**{sheet_name + '__' + journo_name + '__sex':sex_id})\
                            .annotate(n=Count('id'))
                    counts.update({(r['sex'], r['family_role']): r['n'] for r in rows})
            secondary_counts[sex] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, male_female, YESNO, row_perc=True, sec_cols=4)

    def ws_26(self, ws):
        """
        Cols: Sex
        Rows: Whether Quoted
        """
        counts = Counter()
        for model in person_models.itervalues():
            if 'is_quoted' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'is_quoted')\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['is_quoted']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, YESNO, row_perc=True)

    def ws_27(self, ws):
        """
        Cols: Sex
        Rows: Photographed
        """
        counts = Counter()
        for model in person_models.itervalues():
            if 'is_photograph' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', 'is_photograph')\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r['is_photograph']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, IS_PHOTOGRAPH, row_perc=True)

    def ws_28(self, ws):
        """
        Cols: Medium
        Rows: Region
        :: Female reporters only
        """
        counts = Counter()
        for media_type, model in person_models.iteritems():
            region_field = model.sheet_name() + '__country_region__region'
            rows = model.objects\
                    .values(region_field)\
                    .filter(sex=1)\
                    .exclude(**{region_field: 'Unmapped'})\
                    .annotate(n=Count('id'))
            for row in rows:
                if row[region_field] is not None:
                    # Get media and region id's to assign to counts
                    media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                    region_id = [region[0] for region in self.regions if region[1] == row[region_field]][0]

                    counts.update({(media_id, region_id): row['n']})

        self.tabulate(ws, counts, MEDIA_TYPES, self.regions, row_perc=True)

    def ws_29(self, ws):
        """
        Cols: Regions
        Rows: Scope
        :: Female reporters only
        :: Show all countries in regions, irrespective of user selection
        """
        counts = Counter()
        for model in person_models.itervalues():
            sheet_name = model.sheet_name()
            region_field = sheet_name + '__country_region__region'
            scope_field =  sheet_name + '__scope'
            if 'scope' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values(region_field, scope_field)\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .filter(sex=1)\
                        .annotate(n=Count('id'))
                for row in rows:
                    if row[region_field] is not None:
                        region_id = [region[0] for region in self.regions if region[1] == row[region_field]][0]
                        counts.update({(region_id, row[scope_field]): row['n']})

        self.tabulate(ws, counts, self.regions, SCOPE, row_perc=False)

    def ws_30(self, ws):
        """
        Cols: Region
        Rows: Topics
        :: Female reporters only
        :: Show all countries in regions, irrespective of user selection
        """
        counts = Counter()
        for model in person_models.itervalues():
            sheet_name = model.sheet_name()
            region_field = sheet_name + '__country_region__region'
            topic_field =  sheet_name + '__topic'
            if 'topic' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values(region_field, topic_field)\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .filter(sex=1)\
                        .annotate(n=Count('id'))
                for row in rows:
                    if row[region_field] is not None:
                        region_id = [region[0] for region in self.regions if region[1] == row[region_field]][0]
                        counts.update({(region_id, row[topic_field]): row['n']})

        self.tabulate(ws, counts, self.regions, TOPICS, row_perc=False)

    def ws_31(self, ws):
        """
        Cols: Sex of Reporter
        Rows: Topics
        """
        counts = Counter()
        for model in journalist_models.itervalues():
            sheet_name = model.sheet_name()
            topic_field =  sheet_name + '__topic'
            if 'topic' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', topic_field)\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r[topic_field]): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, TOPICS, row_perc=True)

    def ws_32(self, ws):
        """
        Cols: Medium
        Rows: Topics
        :: Female reporters only
        """
        counts = Counter()
        for media_type, model in sheet_models.iteritems():
            if 'topic' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('topic')\
                        .filter(country__in=self.countries)\
                        .filter(**{model.journalist_field_name() + '__sex':1})\
                        .annotate(n=Count('id'))
                for row in rows:
                    media_id = [media[0] for media in MEDIA_TYPES if media[1] == media_type][0]
                    counts.update({(media_id, row['topic']): row['n']})

        self.tabulate(ws, counts, MEDIA_TYPES, TOPICS, row_perc=False)

    def ws_34(self, ws):
        """
        Cols: Sex of reporter
        Rows: Sex of subject
        """
        counts = Counter()
        for model in person_models.itervalues():
            sheet_name = model.sheet_name()
            journo_name = model._meta.get_field(model.sheet_name()).rel.to.journalist_field_name()
            journo_sex = sheet_name + '__' + journo_name + '__sex'
            rows = model.objects\
                    .values(journo_sex, 'sex')\
                    .filter(**{model.sheet_name() + '__country__in':self.countries})\
                    .annotate(n=Count('id'))
            counts.update({(r[journo_sex], r['sex']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, GENDER, row_perc=False)

    def ws_35(self, ws):
        """
        Cols: Sex of reporter
        Rows: Age of reporter
        :: Only for television
        """
        counts = Counter()
        rows = TelevisionJournalist.objects\
                .values('sex', 'age')\
                .filter(television_sheet__country__in=self.countries)\
                .annotate(n=Count('id'))
        counts.update({(r['sex'], r['age']): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, AGES, row_perc=False)

    def ws_36(self, ws):
        """
        Cols: Sex of Reporter
        Rows: Focus: about women
        """
        counts = Counter()
        for model in journalist_models.itervalues():
            sheet_name = model.sheet_name()
            about_women_field =  sheet_name + '__about_women'
            if 'about_women' in model._meta.get_field(sheet_name).rel.to._meta.get_all_field_names():
                rows = model.objects\
                        .values('sex', about_women_field)\
                        .filter(**{model.sheet_name() + '__country__in':self.countries})\
                        .annotate(n=Count('id'))
                counts.update({(r['sex'], r[about_women_field]): r['n'] for r in rows})

        self.tabulate(ws, counts, GENDER, YESNO, row_perc=True)

    def ws_38(self, ws):
        """
        Cols: Focus: about women
        Rows: Topics
        """
        counts = Counter()
        for model in sheet_models.itervalues():
            if 'about_women' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('about_women', 'topic')\
                        .filter(country__in=self.countries)\
                        .annotate(n=Count('id'))
                counts.update({(r['about_women'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, YESNO, TOPICS, row_perc=True)

    def ws_40(self, ws):
        """
        Cols: Focus: about women
        Rows: Region, Topics
        """
        r = 6
        self.write_col_headings(ws, YESNO)

        for region_id, region in self.regions:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'about_women' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('about_women', 'topic')\
                            .filter(country_region__region=region)\
                            .annotate(n=Count('id'))
                    counts.update({(r['about_women'], r['topic']): r['n'] for r in rows})

            self.write_primary_row_heading(ws, region, r=r)
            self.tabulate(ws, counts, YESNO, TOPICS, row_perc=True, sec_row=True, c=1, r=r)
            r += len(TOPICS)

    def ws_41(self, ws):
        """
        Cols: Equality rights raised
        Rows: Topics
        """
        counts = Counter()
        for model in sheet_models.itervalues():
            if 'equality_rights' in model._meta.get_all_field_names():
                rows = model.objects\
                        .values('equality_rights', 'topic')\
                        .filter(country__in=self.countries)\
                        .annotate(n=Count('id'))
                counts.update({(r['equality_rights'], r['topic']): r['n'] for r in rows})
        self.tabulate(ws, counts, YESNO, TOPICS, row_perc=True)

    def ws_42(self, ws):
        """
        Cols: Region
        Rows: Topics, Equality rights raised
        """
        r = 6
        self.write_col_headings(ws, self.regions)

        for topic_id, topic in TOPICS:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'equality_rights' in model._meta.get_all_field_names():
                    rows = model.objects\
                            .values('country_region__region', 'about_women')\
                            .exclude(country_region__region='Unmapped')\
                            .filter(topic=topic_id)\
                            .annotate(n=Count('id'))
                    for row in rows:
                        if row['country_region__region'] is not None:
                            region_id = [region[0] for region in self.regions if region[1] == row['country_region__region']][0]
                            counts.update({(region_id, row['about_women']): row['n']})

            self.write_primary_row_heading(ws, topic, r=r)
            self.tabulate(ws, counts, self.regions, YESNO, row_perc=True, sec_row=True, c=1, r=r)
            r += len(YESNO)

    def ws_43(self, ws):
        """
        Cols: Sex of reporter
        Rows: Topics, Equality rights raised
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        for topic_id, topic in TOPICS:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'equality_rights' in model._meta.get_all_field_names():
                    sex_field = model.journalist_field_name() + '__sex'
                    rows = model.objects\
                            .values(sex_field, 'about_women')\
                            .filter(topic=topic_id)\
                            .annotate(n=Count('id'))
                    counts.update({(r[sex_field], r['about_women']): r['n'] for r in rows})

            self.write_primary_row_heading(ws, topic, r=r)
            self.tabulate(ws, counts, GENDER, YESNO, row_perc=True, sec_row=True, c=1, r=r)
            r += len(YESNO)

    def ws_44(self, ws):
        """
        Cols: Sex of reporter
        Rows: Region, Equality rights raised
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        for region_id, region in self.regions:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'equality_rights' in model._meta.get_all_field_names():
                    sex_field = model.journalist_field_name() + '__sex'
                    rows = model.objects\
                            .values(sex_field, 'about_women')\
                            .filter(country_region__region=region)\
                            .annotate(n=Count('id'))
                    counts.update({(r[sex_field], r['about_women']): r['n'] for r in rows})

            self.write_primary_row_heading(ws, region, r=r)
            self.tabulate(ws, counts, GENDER, YESNO, row_perc=True, sec_row=True, c=1, r=r)
            r += len(YESNO)


    def ws_45(self, ws):
        """
        Cols: Sex of news subject
        Rows: Region, Equality rights raised
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        for region_id, region in self.regions:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'equality_rights' in model._meta.get_all_field_names():
                    sex_field = model.person_field_name() + '__sex'
                    rows = model.objects\
                            .values(sex_field, 'about_women')\
                            .filter(country_region__region=region)\
                            .annotate(n=Count('id'))
                    counts.update({(r[sex_field], r['about_women']): r['n'] for r in rows})

            self.write_primary_row_heading(ws, region, r=r)
            self.tabulate(ws, counts, GENDER, YESNO, row_perc=True, sec_row=True, c=1, r=r)
            r += len(YESNO)

    def ws_46(self, ws):
        """
        Cols: Stereotypes
        Rows: Region, Topics
        """
        r = 6
        self.write_col_headings(ws, AGREE_DISAGREE)

        for region_id, region in self.regions:
            counts = Counter()
            for model in sheet_models.itervalues():
                rows = model.objects\
                        .values('stereotypes', 'topic')\
                        .filter(country_region__region=region)\
                        .annotate(n=Count('id'))
                counts.update({(r['stereotypes'], r['topic']): r['n'] for r in rows})

            self.write_primary_row_heading(ws, region, r=r)
            self.tabulate(ws, counts, AGREE_DISAGREE, TOPICS, row_perc=True, sec_row=True, c=1, r=r)
            r += len(TOPICS)

    def ws_47(self, ws):
        """
        Cols: Stereotypes
        Rows: Topics
        """
        counts = Counter()
        for model in sheet_models.itervalues():
            rows = model.objects\
                    .values('stereotypes', 'topic')\
                    .filter(country__in=self.countries)\
                    .annotate(n=Count('id'))
            counts.update({(r['stereotypes'], r['topic']): r['n'] for r in rows})

        self.tabulate(ws, counts, AGREE_DISAGREE, TOPICS, row_perc=True)

    def ws_48(self, ws):
        """
        Cols: Sex of reporter
        Rows: Topics, Stereotypes
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        for topic_id, topic in TOPICS:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'stereotypes' in model._meta.get_all_field_names():
                    sex_field = model.journalist_field_name() + '__sex'
                    rows = model.objects\
                            .values(sex_field, 'stereotypes')\
                            .filter(country__in=self.countries)\
                            .filter(topic=topic_id)\
                            .annotate(n=Count('id'))
                    counts.update({(r[sex_field], r['stereotypes']): r['n'] for r in rows})

            self.write_primary_row_heading(ws, topic, r=r)
            self.tabulate(ws, counts, GENDER, AGREE_DISAGREE, row_perc=True, sec_row=True, r=r)
            r += len(AGREE_DISAGREE)

    def ws_53(self, ws):
        """
        Cols: Topic
        Rows: Country
        :: Internet media type only
        :: Female reporters only
        """
        filter_cols = [(id, value) for id, value in GENDER if id==1]
        secondary_counts = OrderedDict()
        model = sheet_models.get('Internet News')
        for major_topic, topic_ids in TOPIC_GROUPS.iteritems():
            counts = Counter()
            journo_sex_field = '%s__sex' % model.journalist_field_name()
            rows = model.objects\
                .values(journo_sex_field, 'country')\
                .filter(topic__in=topic_ids)\
                .annotate(n=Count('id'))
            counts.update({(r[journo_sex_field], r['country']): r['n'] for r in rows})
            secondary_counts[major_topic] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.countries, row_perc=True, filter_cols=filter_cols, sec_cols=2)

    def ws_54(self, ws):
        """
        Cols: Major Topic, sex of subject
        Rows: Country
        :: Internet media type only
        """
        secondary_counts = OrderedDict()
        model = person_models.get('Internet News')
        for major_topic, topic_ids in TOPIC_GROUPS.iteritems():
            counts = Counter()
            country_field = '%s__country' % model.sheet_name()
            rows = model.objects\
                .values('sex', country_field)\
                .filter(**{model.sheet_name() + '__topic__in':topic_ids})\
                .annotate(n=Count('id'))
            counts.update({(r['sex'], r[country_field]): r['n'] for r in rows})
            secondary_counts[major_topic] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, GENDER, self.countries, row_perc=True, sec_cols=8)

    def ws_55(self, ws):
        """
        Cols: Occupation
        Rows: Country
        :: Show all countries
        :: Only female subjects
        :: Internet media type only
        """
        counts = Counter()
        model = person_models.get('Internet News')
        country_field = '%s__country' % model.sheet_name()

        rows = model.objects\
                .values(country_field, 'occupation')\
                .filter(sex=1)\
                .annotate(n=Count('id'))

        counts.update({(r['occupation'], r[country_field]): r['n'] for r in rows})
        self.tabulate(ws, counts, OCCUPATION, self.countries, row_perc=True)

    def ws_56(self, ws):
        """
        Cols: Function
        Rows: Country
        :: Show all countries
        :: Internet media type only
        """
        counts = Counter()
        model = person_models.get('Internet News')
        country_field = '%s__country' % model.sheet_name()
        rows = model.objects\
                .values(country_field, 'function')\
                .annotate(n=Count('id'))

        counts.update({(r['function'], r[country_field]): r['n'] for r in rows})
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
        model = person_models.get('Internet News')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'family_role')\
                    .filter(**{model.sheet_name() + '__country':code})\
                    .annotate(n=Count('id'))

            counts = {(row['sex'], row['family_role']): row['n'] for row in rows}
            # If only captured countries should be displayed use
            # if counts.keys():
            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, YESNO, row_perc=True, sec_row=True, r=r)
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
        model = person_models.get('Internet News')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'is_photograph')\
                    .filter(**{model.sheet_name() + '__country':code})\
                    .annotate(n=Count('id'))
            counts = {(row['sex'], row['is_photograph']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, IS_PHOTOGRAPH, row_perc=True, sec_row=True, r=r)
            r += len(IS_PHOTOGRAPH)

    def ws_59(self, ws):
        """
        Cols: Sex of reporter
        Rows: Sex of subject
        :: Internet media only
        """
        counts = Counter()
        model = person_models.get('Internet News')
        sheet_name = model.sheet_name()
        journo_name = model._meta.get_field(model.sheet_name()).rel.to.journalist_field_name()
        journo_sex = sheet_name + '__' + journo_name + '__sex'

        rows = model.objects\
                .values(journo_sex, 'sex')\
                .filter(**{model.sheet_name() + '__country__in':self.countries})\
                .annotate(n=Count('id'))
        counts.update({(r[journo_sex], r['sex']): r['n'] for r in rows})

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
        model = person_models.get('Internet News')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'age')\
                    .filter(**{model.sheet_name() + '__country':code})\
                    .annotate(n=Count('id'))
            counts = {(row['sex'], row['age']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, AGES, row_perc=True, sec_row=True, r=r)
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
        model = person_models.get('Internet News')
        for code, country in self.countries:
            rows = model.objects\
                    .values('sex', 'is_quoted')\
                    .filter(**{model.sheet_name() + '__country':code})\
                    .annotate(n=Count('id'))
            counts = {(row['sex'], row['is_quoted']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, GENDER, YESNO, row_perc=True, sec_row=True, r=r)
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
        model = sheet_models.get('Internet News')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'equality_rights')\
                    .filter(country=code)\
                    .annotate(n=Count('id'))
            counts = {(row['topic'], row['equality_rights']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, YESNO, row_perc=True, sec_row=True, r=r)
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
        model = sheet_models.get('Internet News')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'stereotypes')\
                    .filter(country=code)\
                    .annotate(n=Count('id'))
            counts = {(row['topic'], row['stereotypes']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, AGREE_DISAGREE, row_perc=True, sec_row=True, r=r)
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
        model = sheet_models.get('Internet News')
        for code, country in self.countries:
            rows = model.objects\
                    .values('topic', 'about_women')\
                    .filter(country=code)\
                    .annotate(n=Count('id'))
            counts = {(row['topic'], row['about_women']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, YESNO, row_perc=True, sec_row=True, r=r)
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
                    .filter(country=code)\
                    .annotate(n=Count('id'))
            counts = {(row['topic'], row['retweet']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, RETWEET, row_perc=False, sec_row=True, r=r)
            r += len(RETWEET)

    def ws_66(self, ws):
        """
        Cols: Topic
        Rows: Country, sex of news subject
        :: Show all countries
        :: Twitter media type only
        """
        r = 6
        self.write_col_headings(ws, GENDER)

        counts = Counter()
        model = person_models.get('Twitter')
        topic_field = '%s__topic' % model.sheet_name()
        for code, country in self.countries:
            rows = model.objects\
                    .values(topic_field, 'sex')\
                    .filter(**{model.sheet_name() + '__country':code})\
                    .annotate(n=Count('id'))
            counts.update({(row[topic_field], row['sex']): row['n'] for row in rows})

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, GENDER, row_perc=True, sec_row=True, r=r)
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
                .filter(**{model.journalist_field_name() + '__sex':1})\
                .annotate(n=Count('id'))
        counts.update({(row['topic'], row['country']): row['n'] for row in rows})

        self.tabulate(ws, counts, TOPICS, self.countries, row_perc=True, sec_row=False)

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
                    .filter(country=code)\
                    .annotate(n=Count('id'))
            counts = {(row['topic'], row['about_women']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, YESNO, row_perc=False, sec_row=True, r=r)
            r += len(YESNO)

    def ws_69(self, ws):
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
                    .filter(country=code)\
                    .annotate(n=Count('id'))
            counts = {(row['topic'], row['stereotypes']): row['n'] for row in rows}

            self.write_primary_row_heading(ws, country, r=r)
            self.tabulate(ws, counts, TOPICS, AGREE_DISAGREE, row_perc=True, sec_row=True, r=r)
            r += len(AGREE_DISAGREE)

    def ws_76(self, ws):
        """
        Cols: Topic, Stereotypes
        Rows: Country
        """
        secondary_counts = OrderedDict()
        for topic_id, topic in TOPICS:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'stereotypes' in model._meta.get_all_field_names():
                    rows = model.objects\
                        .values('stereotypes', 'country')\
                        .filter(topic=topic_id)\
                        .annotate(n=Count('id'))
                    counts.update({(r['stereotypes'], r['country']): r['n'] for r in rows})
                secondary_counts[topic] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, AGREE_DISAGREE, self.countries, row_perc=True, sec_cols=8)

    def ws_77(self, ws):
        """
        Cols: Topic, Reference to gender equality
        Rows: Country
        """
        secondary_counts = OrderedDict()
        for topic_id, topic in TOPICS:
            counts = Counter()
            for model in sheet_models.itervalues():
                if 'equality_rights' in model._meta.get_all_field_names():
                    rows = model.objects\
                        .values('equality_rights', 'country')\
                        .filter(topic=topic_id)\
                        .annotate(n=Count('id'))
                    counts.update({(r['equality_rights'], r['country']): r['n'] for r in rows})
                secondary_counts[topic] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, YESNO, self.countries, row_perc=True, sec_cols=4)

    def ws_78(self, ws):
        """
        Cols: Topic, victim_of
        Rows: Country
        """
        secondary_counts = OrderedDict()
        for topic_id, topic in TOPICS:
            counts = Counter()
            for model in person_models.itervalues():
                if 'victim_of' in model._meta.get_all_field_names():
                    country_field = '%s__country' % model.sheet_name()
                    rows = model.objects\
                        .values('victim_of', country_field)\
                        .filter(**{model.sheet_name() + '__topic':topic_id})\
                        .annotate(n=Count('id'))
                    counts.update({(r['victim_of'], r[country_field]): r['n'] for r in rows})
                secondary_counts[topic] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, VICTIM_OF, self.countries, row_perc=True, sec_cols=18)

    def ws_79(self, ws):
        """
        Cols: Topic, survivor_of
        Rows: Country
        """
        secondary_counts = OrderedDict()
        for topic_id, topic in TOPICS:
            counts = Counter()
            for model in person_models.itervalues():
                if 'survivor_of' in model._meta.get_all_field_names():
                    country_field = '%s__country' % model.sheet_name()
                    rows = model.objects\
                        .values('survivor_of', country_field)\
                        .filter(**{model.sheet_name() + '__topic':topic_id})\
                        .annotate(n=Count('id'))
                    counts.update({(r['survivor_of'], r[country_field]): r['n'] for r in rows})
                secondary_counts[topic] = counts

        self.tabulate_secondary_cols(ws, secondary_counts, SURVIVOR_OF, self.countries, row_perc=True, sec_cols=18)

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


    def tabulate_secondary_cols(self, ws, secondary_counts, cols, rows, row_perc=False, filter_cols=None, sec_cols=4):
        """
        :param ws: worksheet to write to
        :param secondary_counts: dict in following format:
            {'Primary column heading': Count object, ...}
        :param list cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param list rows: list of `(row_id, row_title)` tuples of row ids and titles
        :param bool row_perc: should percentages by calculated by row instead of column (default: False)
        :param sec_cols: amount of cols needed for secondary cols
        """
        r, c = 7, 1

        # row titles
        for i, row in enumerate(rows):
            row_id, row_title = row
            ws.write(r + i, c, clean_title(row_title))
        c += 1

        for field, counts in secondary_counts.iteritems():
            ws.write(r - 3, c, clean_title(field))
            self.tabulate(ws, counts, cols, rows, row_perc=row_perc, sec_col=True, filter_cols=filter_cols, r=7, c=c)
            c += sec_cols

    def write_col_headings(self, ws, cols, c=2, r=4):
        """
        :param ws: worksheet to write to
        :param cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param r, c: initial position where cursor should start writing to

        """
        for col_id, col_title in cols:
            ws.write(r, c, clean_title(col_title))
            ws.write(r + 1, c, "N")
            ws.write(r + 1, c + 1, "%")
            c += 2

    def write_primary_row_heading(self, ws, heading, c=0, r=6):
        """
        :param ws: worksheet to write to
        :param heading: row heading to write
        :param r, c: position where heading should be written to

        """
        ws.write(r, c, clean_title(heading))


    def tabulate(self, ws, counts, cols, rows, row_perc=False, sec_col=False, sec_row=False, filter_cols=None, c=1, r=6):
        """ Emit a table.

        :param ws: worksheet to write to
        :param dict counts: dict from `(col_id, row_id)` tuples to count for that combination.
        :param list cols: list of `(col_id, col_title)` tuples of column ids and titles
        :param list rows: list of `(row_id, row_title)` tuples of row ids and titles
        :param bool row_perc: should percentages by calculated by row instead of column (default: False)
        :param sec_col: Are wecreating a secondary column title(default: False)
        :param sec_row: Are we creating a secondary row title(default: False)
        :param r, c: initial position where cursor should start writing to
        """
        if row_perc:
            # we'll need percentage by rows
            row_totals = {}
            for row_id, row_title in rows:
                row_totals[row_id] = sum(counts.get((col_id, row_id), 0) for col_id, _ in cols)  # noqa

        # row titles
        if not sec_col:
            # Else already written
            for i, row in enumerate(rows):
                row_id, row_title = row
                ws.write(r + i, c, clean_title(row_title))

            c += 1

        # if only filtered results should be shown
        # e.g. only print female columns
        if filter_cols:
            cols = filter_cols

        # values, written by column
        for col_id, col_title in cols:
            # column title
            if not sec_row:
                # Else already written
                ws.write(r - 2, c, clean_title(col_title))
                ws.write(r - 1, c, "N")
                ws.write(r - 1, c + 1, "%")

            if not row_perc:
                # column totals
                # Confirm: Perc of col total or matrix total?
                # total = sum(counts.itervalues())
                total = sum(counts.get((col_id, row_id), 0) for row_id, _ in rows)

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
