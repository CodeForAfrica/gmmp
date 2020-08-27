# Python
import io

# Django
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

# 3rd Party
import xlsxwriter

# Project
from forms.models import (
    person_models, sheet_models, journalist_models)
from forms.modelutils import (TOPICS, GENDER, SPACE, OCCUPATION, FUNCTION, SCOPE,
    AGES, SOURCE, VICTIM_OF, SURVIVOR_OF, IS_PHOTOGRAPH, AGREE_DISAGREE,
    RETWEET)


class XLSXDataExportBuilder():
    def __init__(self, request):
        self.domain = "http://%s" % get_current_site(request).domain

        self.sheet_exclude_fields = ['monitor', 'url_and_multimedia', 'time_accessed', 'country_region']
        self.person_exclude_fields = []
        self.journalist_exclude_fields =[]

        self.sheet_fields_with_id = ['topic', 'scope', 'inequality_women', 'stereotypes']
        self.person_fields_with_id = ['sex', 'age', 'occupation', 'function', 'survivor_of', 'victim_of']
        self.journalist_fields_with_id = ['sex', 'age']


    def build(self):
        """
        Generate an Excel spreadsheet and return it as a string.
        """
        output = io.StringIO()
        workbook = xlsxwriter.Workbook(output)

        for model in sheet_models.values():
            self.create_sheet_export(model, workbook)

        for model in person_models.values():
            self.create_person_export(model, workbook)

        for model in journalist_models.values():
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
                ws.write(row, col, str(field.name))
                col += 1
                if field.name in fields_with_id:
                    ws.write(row, col, str(field.name+"_id"))
                    col += 1
            ws.write(row, col, str('edit_url'))
            col += 1
        else:
            for field in fields:
                ws.write(row, col, str("sheet_" + field.name))
                col += 1
                if field.name in fields_with_id:
                    ws.write(row, col, str("sheet_" + field.name + "_id"))
                    col += 1
            ws.write(row, col, str('sheet_edit_url'))
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
                ws.write(row, col, str(TOPICS[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, TOPICS[getattr(obj, field.name)-1][0])
            elif field.name == 'scope':
                ws.write(row, col, str(SCOPE[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, SCOPE[getattr(obj, field.name)-1][0])
            elif field.name == 'inequality_women':
                ws.write(row, col, str(AGREE_DISAGREE[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, AGREE_DISAGREE[getattr(obj, field.name)-1][0])
            elif field.name == 'stereotypes':
                ws.write(row, col, str(AGREE_DISAGREE[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, AGREE_DISAGREE[getattr(obj, field.name)-1][0])
            elif field.name == 'space':
                ws.write(row, col, str(SPACE[getattr(obj, field.name)-1][1]))
            elif field.name == 'retweet':
                ws.write(row, col, str(RETWEET[getattr(obj, field.name)-1][1]))
            else:
                try:
                    ws.write(row, col, str(getattr(obj, field.name)))
                    if field.name in fields_with_id:
                        col += 1
                except UnicodeEncodeError:
                    ws.write(row, col, str(getattr(obj, field.name).encode('ascii', 'replace')))
            col += 1
        change_url = reverse(
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
                ws.write(row, col, str(GENDER[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, GENDER[getattr(obj, field.name)-1][0])
            elif field.name == 'age':
                ws.write(row, col, str(AGES[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, AGES[getattr(obj, field.name)][0])
            elif field.name == 'occupation':
                ws.write(row, col, str(OCCUPATION[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, OCCUPATION[getattr(obj, field.name)][0])
            elif field.name == 'function':
                ws.write(row, col, str(FUNCTION[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, FUNCTION[getattr(obj, field.name)][0])
            elif field.name == 'victim_of' and not getattr(obj, field.name) == None:
                ws.write(row, col, str(VICTIM_OF[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, VICTIM_OF[getattr(obj, field.name)][0])
            elif field.name == 'survivor_of' and not getattr(obj, field.name) == None:
                ws.write(row, col, str(SURVIVOR_OF[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, SURVIVOR_OF[getattr(obj, field.name)][0])
            elif field.name == 'is_photograph':
                ws.write(row, col, str(IS_PHOTOGRAPH[getattr(obj, field.name)-1][1]))
            elif field.name == 'space':
                ws.write(row, col, str(SPACE[getattr(obj, field.name)-1][1]))
            elif field.name == 'retweet':
                ws.write(row, col, str(RETWEET[getattr(obj, field.name)-1][1]))
            elif field.name == obj.sheet_name():
                ws.write(row, col, getattr(obj, field.name).id)
                # Get the parent model and id for building the edit link
                parent_model = field.related.parent_model
                parent_id = getattr(obj, field.name).id
            else:
                try:
                    ws.write(row,col, str(getattr(obj, field.name)))
                    if field.name in self.person_fields_with_id:
                        col += 1
                except UnicodeEncodeError:
                    ws.write(row,col, str(getattr(obj, field.name).encode('ascii', 'replace')))
            col += 1
        # Write link to end of row
        change_url = reverse(
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
                ws.write(row, col, str(GENDER[getattr(obj, field.name)-1][1]))
                col += 1
                ws.write(row, col, GENDER[getattr(obj, field.name)-1][0])
            elif field.name == 'age' and not getattr(obj, field.name) == None:
                ws.write(row, col, str(AGES[getattr(obj, field.name)][1]))
                col += 1
                ws.write(row, col, AGES[getattr(obj, field.name)][0])
            elif field.name == obj.sheet_name():
                ws.write(row, col, getattr(obj, field.name).id)
                # Get the parent model and id for building the edit link
                parent_model = field.related.parent_model
                parent_id = getattr(obj, field.name).id
            else:
                try:
                    ws.write(row,col, str(getattr(obj, field.name)))
                    if field.name in fields_with_id:
                        col += 1
                except UnicodeEncodeError:
                    ws.write(row,col, str(getattr(obj, field.name).encode('ascii', 'replace')))
            col += 1
        # Write link to end of row
        change_url = reverse(
            'admin:%s_%s_change' % (
                parent_model._meta.app_label,
                parent_model._meta.model_name),
            args=(parent_id,))
        ws.write_url(row, col, "%s%s" % (self.domain, change_url))

        return ws, col
