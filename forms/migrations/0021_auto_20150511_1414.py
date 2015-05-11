# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
    ]
