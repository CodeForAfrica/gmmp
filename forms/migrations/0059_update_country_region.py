# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

COUNTRY_REGION = [
    ("Myanmar", "Asia"),
    ("Angola","Africa"),
    ("Cambodia","Asia"),
    ("Cayman Islands","Caribbean"),
    ("Dominica","Caribbean"),
    ("Greenland","Europe"),
    ("Honduras","Latin America"),
    ("Hong Kong","Asia"),
    ("Iraq","Middle East"),
    ("Jordan","Middle East"),
    ("Macao","Asia"),
    ("Papua New Guinea","Pacific"),
    ("Russia","Europe"),
    ("Rwanda","Africa"),
    ("Seychelles","Africa"),
    ("Timor-Leste","Asia"),
    ("Uzbekistan","Asia"),
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

    # Update Regions
    CountryRegion.objects.using(db_alias).filter(region="Pacific Islands").update(region="Pacific")
    CountryRegion.objects.using(db_alias).filter(region="Pacific Islands").update(region="Pacific")

    # Update countries regions
    CountryRegion.objects.using(db_alias).filter(country="CY").update(region="Europe")
    CountryRegion.objects.using(db_alias).filter(country="KZ").update(region="Asia")
    CountryRegion.objects.using(db_alias).filter(country="PR").update(region="Caribbean")
    CountryRegion.objects.using(db_alias).filter(country="VU").update(region="Pacific")

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
    # Reverse Update regions
    CountryRegion.objects.using(db_alias).filter(country="CY").update(region="Middle East")
    CountryRegion.objects.using(db_alias).filter(country="KZ").update(region="Europe")
    
    # Delete CountryRegion objects for supplied pairs
    region_map = get_region_map(CountryRegion)
    for region, country_code_list in region_map.items():
        for country_code in country_code_list:
            CountryRegion.objects.using(db_alias).filter(
                country=country_code, region=region
            ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0058_add_deleted_attribute"),
    ]

    operations = [
         migrations.RunPython(code, reverse_code),
    ]
