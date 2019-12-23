# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django_countries import countries

def populate_weights(apps, schema_editor):
    Weights = apps.get_model("reports", "Weights")
    db_alias = schema_editor.connection.alias

    for item in COUNTRY_WEIGHTS:
        country = item['Country']
        item.pop('Country')
        for media_type, weight in item.items():
            w = Weights.objects.using(db_alias).create(
                    country=country,
                    media_type=media_type,
                    weight=weight)
            w.save()

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_indonesia-weights'),
    ]

    operations = [
        migrations.RunPython(
                populate_weights,
                backwards,
            ),
    ]

COUNTRY_WEIGHTS= [
{'Country': 'T1',
  'Internet': '1',
  'Print': '1',
  'Radio': '1',
  'Television': '1',
  'Twitter': '1'}]
