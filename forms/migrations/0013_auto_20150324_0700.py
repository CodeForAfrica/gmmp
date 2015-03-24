# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0012_auto_20150312_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internetnewssheet',
            name='country',
        ),
        migrations.RemoveField(
            model_name='internetnewssheet',
            name='monitor',
        ),
        migrations.RemoveField(
            model_name='newspapersheet',
            name='country',
        ),
        migrations.RemoveField(
            model_name='newspapersheet',
            name='monitor',
        ),
        migrations.RemoveField(
            model_name='radiosheet',
            name='country',
        ),
        migrations.RemoveField(
            model_name='radiosheet',
            name='monitor',
        ),
        migrations.RemoveField(
            model_name='televisionsheet',
            name='country',
        ),
        migrations.RemoveField(
            model_name='televisionsheet',
            name='monitor',
        ),
        migrations.RemoveField(
            model_name='twittersheet',
            name='country',
        ),
        migrations.RemoveField(
            model_name='twittersheet',
            name='monitor',
        ),
    ]
