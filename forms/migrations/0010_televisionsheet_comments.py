# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0009_auto_20150312_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='televisionsheet',
            name='comments',
            field=models.TextField(verbose_name='Describe any photographs included in the story and the conclusions you draw from them.', blank=True),
            preserve_default=True,
        ),
    ]
