# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0032_auto_20191212_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radiosheet',
            name='num_female_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other</strong>', verbose_name='Number of female anchors'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='num_female_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other</strong>', verbose_name='Number of female anchors'),
            preserve_default=True,
        ),
    ]
