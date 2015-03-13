# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0011_auto_20150312_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetnewssheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
    ]
