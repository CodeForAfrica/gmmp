# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

COUNTRY_REGION = [
    ("North Ireland", "Europe"),
    ("International", "Global"),
]


def get_region_map(CountryRegion):
    from django_countries import countries

    region_map = {}

    # Map new country code(s) to regions
    for country_region in COUNTRY_REGION:
        code = countries.by_name(country_region[0])
        if code:
            if country_region[1] in region_map:
                region_map[country_region[1]].append(code)
            else:
                region_map[country_region[1]] = [code]

    return region_map


def code(apps, schema_editor):

    CountryRegion = apps.get_model("forms", "CountryRegion")
    db_alias = schema_editor.connection.alias

    country_region_objs = CountryRegion.objects.using(db_alias).all()

    # Update old custom country codes to ISO use-assignable codes
    CountryRegion.objects.using(db_alias).filter(country="B1").update(country="QM")
    CountryRegion.objects.using(db_alias).filter(country="B2").update(country="QN")
    CountryRegion.objects.using(db_alias).filter(country="EN").update(country="QO")
    CountryRegion.objects.using(db_alias).filter(country="SQ").update(country="QQ")
    CountryRegion.objects.using(db_alias).filter(country="WL").update(country="QR")

    # Create CountryRegion objects for supplied pairs
    region_map = get_region_map(CountryRegion)
    for region, country_code_list in region_map.items():
        for country_code in country_code_list:
            CountryRegion.objects.using(db_alias).create(
                country=country_code, region=region
            )


def reverse_code(apps, schema_editor):
    CountryRegion = apps.get_model("forms", "CountryRegion")
    db_alias = schema_editor.connection.alias

    # Revert ISO use-assignable codes to  old custom country codes
    CountryRegion.objects.using(db_alias).filter(country="QM").update(country="B1")
    CountryRegion.objects.using(db_alias).filter(country="QN").update(country="B2")
    CountryRegion.objects.using(db_alias).filter(country="QO").update(country="EN")
    CountryRegion.objects.using(db_alias).filter(country="QQ").update(country="SQ")
    CountryRegion.objects.using(db_alias).filter(country="QR").update(country="WL")

    # Delete CountryRegion objects for supplied pairs
    region_map = get_region_map(CountryRegion)
    for region, country_code_list in region_map.items():
        for country_code in country_code_list:
            CountryRegion.objects.using(db_alias).filter(
                country=country_code, region=region
            ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0042_auto_20200220_1247"),
    ]

    operations = [
        migrations.RunPython(code, reverse_code),
    ]
