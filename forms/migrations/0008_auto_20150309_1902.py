# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_auto_20150309_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='televisionsheet',
            name='television_channel',
            field=models.CharField(help_text="Be as specific as possible. E.g. if the television company is called RTV, and if the newscast is broadcast on its second channel, write in 'RTV-2' ", max_length=255, verbose_name='Channel'),
            preserve_default=True,
        ),
    ]
