# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Weights',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('media_type', models.CharField(max_length=32)),
                ('weight', models.DecimalField(max_digits=4, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
