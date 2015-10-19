# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


def assign_transnational_region_to_sheets(apps, schema_editor):
    from forms.models import sheet_models

    CountryRegion = apps.get_model("forms", "CountryRegion")
    Monitor = apps.get_model("gmmp", "Monitor")

    db_alias = schema_editor.connection.alias

    try:
        trans_country_region = CountryRegion.objects.using(db_alias).get(country='T1', region='Transnational')
    except ObjectDoesNotExist:
        trans_country_region = CountryRegion(country='T1', region='Transnational')
        trans_country_region.save()

    monitor = Monitor.objects.get(user__last_name='Macharia', user__first_name='Sarah')
    monitor.country = trans_country_region.country
    monitor.save()

    for name, model in sheet_models.iteritems():
        sheets_model = apps.get_model("forms", model._meta.object_name)
        sheets = sheets_model.objects.using(db_alias).filter(monitor=monitor)
        for sheet in sheets:
            sheet.country_region = trans_country_region
            sheet.country = trans_country_region.country
            sheet.save()

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0022_assign_country_region_to_sheet_models'),
    ]

    operations = [
        migrations.RunPython(
                assign_transnational_region_to_sheets,
                backwards,
            ),
    ]
