# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0025_auto_20191210_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internetnewssheet',
            name='person_secondary',
        ),
    ]
