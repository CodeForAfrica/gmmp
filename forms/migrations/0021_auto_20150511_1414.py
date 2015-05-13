# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

COUNTRY_REGION = [
    ("Afghanistan","Asia"),
    ("Albania","Europe"),
    ("Antigua and Barbuda","Carribean"),
    ("Argentina","Latin America"),
    ("Armenia","Europe"),
    ("Australia","Pacific Islands"),
    ("Austria","Europe"),
    ("Bahamas","Carribean"),
    ("Bangladesh","Asia"),
    ("Barbados","Carribean"),
    ("Belarus","Europe"),
    ("Belgium","Europe"),
    ("Belize","Carribean"),
    ("Benin","Africa"),
    ("Bhutan","Asia"),
    ("Bolivia","Latin America"),
    ("Bosnia and Herzegovina","Europe"),
    ("Botswana","Africa"),
    ("Brazil","Latin America"),
    ("Bulgaria","Europe"),
    ("Burkina Faso","Africa"),
    ("Burundi","Africa"),
    ("Cameroon","Africa"),
    ("Canada","North America"),
    ("Cabo Verde","Africa"),
    ("Central African Republic","Africa"),
    ("Chad","Africa"),
    ("Chile","Latin America"),
    ("China","Asia"),
    ("Colombia","Latin America"),
    ("Comoros","Africa"),
    ("Congo (the Democratic Republic of the)","Africa"),
    ("Congo","Africa"),
    ("Costa Rica","Latin America"),
    ("Croatia","Europe"),
    ("Cuba","Carribean"),
    ("Cyprus","Middle East"),
    ("Denmark","Europe"),
    ("Dominican Republic","Carribean"),
    ("Ecuador","Latin America"),
    ("Egypt","Middle East"),
    ("El Salvador","Latin America"),
    ("Equatorial Guinea","Africa"),
    ("Estonia","Europe"),
    ("Ethiopia","Africa"),
    ("Fiji","Pacific Islands"),
    ("Finland","Europe"),
    ("France","Europe"),
    ("Gabon","Africa"),
    ("Gambia (The)","Africa"),
    ("Georgia","Europe"),
    ("Germany","Europe"),
    ("Ghana","Africa"),
    ("Greece","Europe"),
    ("Grenada","Carribean"),
    ("Guatemala","Latin America"),
    ("Guinea-Bissau","Africa"),
    ("Guinea","Africa"),
    ("Guyana","Carribean"),
    ("Haiti","Carribean"),
    ("Hungary","Europe"),
    ("Iceland","Europe"),
    ("India","Asia"),
    ("Ireland","Europe"),
    ("Israel","Middle East"),
    ("Italy","Europe"),
    (u"C\xf4te d'Ivoire","Africa"),
    ("Jamaica","Carribean"),
    ("Japan","Asia"),
    ("Kazakhstan","Europe"),
    ("Kenya","Africa"),
    ("Kyrgyzstan","Asia"),
    ("Lebanon","Middle East"),
    ("Lesotho","Africa"),
    ("Liberia","Africa"),
    ("Luxembourg","Europe"),
    ("Macedonia","Europe"),
    ("Madagascar","Africa"),
    ("Malawi","Africa"),
    ("Malaysia","Asia"),
    ("Mali","Africa"),
    ("Malta","Europe"),
    ("Mauritania","Africa"),
    ("Mauritius","Africa"),
    ("Mexico","Latin America"),
    ("Moldovia","Europe"),
    ("Mongolia","Asia"),
    ("Montenegro","Europe"),
    ("Morocco","Middle East"),
    ("Namibia","Africa"),
    ("Nepal","Asia"),
    ("Netherlands","Europe"),
    ("New Zealand","Pacific Islands"),
    ("Nicaragua","Latin America"),
    ("Niger","Africa"),
    ("Nigeria","Africa"),
    ("Norway","Europe"),
    ("Pakistan","Asia"),
    ("Palestine, State of","Middle East"),
    ("Paraguay","Latin America"),
    ("Peru","Latin America"),
    ("Philippines","Asia"),
    ("Poland","Europe"),
    ("Portugal","Europe"),
    ("Puerto Rico","Latin America"),
    ("Romania","Europe"),
    ("Samoa","Pacific Islands"),
    ("Senegal","Africa"),
    ("Serbia","Europe"),
    ("Sierra Leone","Africa"),
    ("Slovakia","Europe"),
    ("Slovenia","Europe"),
    ("Solomon Islands","Pacific Islands"),
    ("Somalia","Africa"),
    ("South Africa","Africa"),
    ("South Korea","Asia"),
    ("Spain","Europe"),
    ("Saint Lucia","Carribean"),
    ("Saint Vincent and the Grenadines","Carribean"),
    ("Sudan","Africa"),
    ("South Sudan","Africa"),
    ("Suriname","Carribean"),
    ("Swaziland","Africa"),
    ("Sweden","Europe"),
    ("Switzerland","Europe"),
    ("Taiwan","Asia"),
    ("Tanzania","Africa"),
    ("Togo","Africa"),
    ("Tonga","Pacific Islands"),
    ("Trinidad and Tobago","Carribean"),
    ("Tunisia","Middle East"),
    ("Turkey","Europe"),
    ("Uganda","Africa"),
    ("United Kingdom","Europe"),
    ("United States","North America"),
    ("Uruguay","Latin America"),
    ("Vanuatu","Asia"),
    ("Venezuela","Latin America"),
    ("Vietnam","Asia"),
    ("Zambia","Africa"),
    ("Zimbabwe","Africa")
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

    # Create CountryRegion for unmapped countries
    if not country_region_objs.filter(country="ZZ"):
        CountryRegion.objects.using(db_alias).create(
            country="ZZ",
            region="Unmapped")

    # Create CountryRegion objects for supplied pairs
    for region, countries in region_map.iteritems():
        for country in countries:
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
        ('forms', '0020_auto_20150506_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryRegion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(unique=True, max_length=2)),
                ('region', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='internetnewssheet',
            name='country_region',
            field=models.ForeignKey(to='forms.CountryRegion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newspapersheet',
            name='country_region',
            field=models.ForeignKey(to='forms.CountryRegion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='radiosheet',
            name='country_region',
            field=models.ForeignKey(to='forms.CountryRegion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='televisionsheet',
            name='country_region',
            field=models.ForeignKey(to='forms.CountryRegion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twittersheet',
            name='country_region',
            field=models.ForeignKey(to='forms.CountryRegion', null=True),
            preserve_default=True,
        ),

        migrations.RunPython(
            populate_country_region,
            backwards,
        ),
    ]
