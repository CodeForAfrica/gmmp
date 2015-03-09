# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_auto_20150309_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='internetnewsperson',
            name='age',
            field=models.PositiveIntegerField(default=None, verbose_name='Age (person appears)', choices=[(0, 'Do not know'), (1, '12 and under'), (2, '13-18'), (3, '19-34'), (4, '35-49'), (5, '50-64'), (6, '65 years or more')]),
            preserve_default=False,
        ),
    ]
