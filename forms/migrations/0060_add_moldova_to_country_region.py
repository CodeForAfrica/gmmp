# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

COUNTRY_REGION = [
    ("Moldova", "Europe"),
]

def populate_country_region(apps, schema_editor):
    from django_countries import countries
    CountryRegion = apps.get_model("forms", "CountryRegion")
    db_alias = schema_editor.connection.alias

    country_region_objs = CountryRegion.objects.using(db_alias).all()
    region_map = {}

    # Map country codes to regions
    for country_region in COUNTRY_REGION:
        code = countries.by_name(country_region[0])
        if code:
            if country_region[1] in region_map:
                region_map[country_region[1]].append(code)
            else:
                region_map[country_region[1]] = [code]

    # Create CountryRegion objects for supplied pairs
    for region, country_list in region_map.items():
        for country in country_list:
            # Is this check necessary?
            if not country_region_objs.filter(country=country):
                CountryRegion.objects.using(db_alias).create(
                    country=country,
                    region=region)


def backwards(apps, schema_editor):
    """
    Table gets dropped, so no need to delete the rows
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0059_update_country_region"),
    ]

    operations = [
         migrations.RunPython(populate_country_region, backwards),
    ]
