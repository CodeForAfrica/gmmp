# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def assign_country_region_to_sheet(apps, schema_editor):
    from forms.models import sheet_models

    CountryRegion = apps.get_model("forms", "CountryRegion")
    db_alias = schema_editor.connection.alias

    for name, model in sheet_models.iteritems():
        sheets_model = apps.get_model("forms", model._meta.object_name)
        sheets = sheets_model.objects.using(db_alias).all()
        for sheet in sheets:
            try:
                country_region = CountryRegion.objects.using(db_alias).get(country=sheet.country.code)
                sheet.country_region = country_region
                sheet.save()
            except CountryRegion.DoesNotExist:
                # Assign to unmapped CountryRegion object
                country_region = CountryRegion.objects.using(db_alias).get(region='Unmapped')
                sheet.country_region = country_region
                sheet.save()

def backwards(apps, schema_editor):
    from forms.models import sheet_models
    db_alias = schema_editor.connection.alias

    for name, model in sheet_models.iteritems():
        sheets_model = apps.get_model("forms", model._meta.object_name)
        sheets = sheets_model.objects.using(db_alias).all()
        for sheet in sheets:
            sheet.country_region = None
            sheet.save()

class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0021_auto_20150511_1414'),
    ]

    operations = [
        migrations.RunPython(
                assign_country_region_to_sheet,
                backwards,
            ),
    ]
