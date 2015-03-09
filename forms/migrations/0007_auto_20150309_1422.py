# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_auto_20150309_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='televisionsheet',
            old_name='television_station',
            new_name='television_channel',
        ),
        migrations.RemoveField(
            model_name='televisionsheet',
            name='person_secondary',
        ),
    ]
