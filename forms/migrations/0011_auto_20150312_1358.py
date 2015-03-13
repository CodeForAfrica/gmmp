# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0010_televisionsheet_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='internetnewssheet',
            name='country',
            field=django_countries.fields.CountryField(default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newspapersheet',
            name='country',
            field=django_countries.fields.CountryField(default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='radiosheet',
            name='country',
            field=django_countries.fields.CountryField(default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='televisionsheet',
            name='country',
            field=django_countries.fields.CountryField(default=None, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twittersheet',
            name='country',
            field=django_countries.fields.CountryField(default=None, max_length=2),
            preserve_default=False,
        ),
    ]
