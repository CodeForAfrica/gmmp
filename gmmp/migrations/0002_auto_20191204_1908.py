# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gmmp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='country',
            field=django_countries.fields.CountryField(default=b'KE', max_length=2),
            preserve_default=True,
        ),
    ]
