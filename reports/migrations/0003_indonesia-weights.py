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
        for media_type, weight in item.iteritems():
            w = Weights.objects.using(db_alias).create(
                    country=country,
                    media_type=media_type,
                    weight=weight)
            w.save()

def backwards(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_populate_weights'),
    ]

    operations = [
        migrations.RunPython(
                populate_weights,
                backwards,
            ),
    ]

COUNTRY_WEIGHTS= [
{'Country': 'ID',
  'Internet': '0',
  'Print': '11',
  'Radio': '1',
  'Television': '7',
  'Twitter': '0'}]
