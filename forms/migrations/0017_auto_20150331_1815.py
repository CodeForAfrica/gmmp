# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0016_auto_20150330_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radiosheet',
            name='item_number',
            field=models.PositiveIntegerField(help_text='Write in the number that describes the position of the story within the newscast. E.g. the first story in the newscast is item 1; the seventh story is item 7.', verbose_name='(1) Item Number', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='item_number',
            field=models.PositiveIntegerField(help_text='Write in the number that describes the position of the story within the newscast. E.g. the first story in the newscast is item 1; the seventh story is item 7.', verbose_name='(1) Item Number', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29)]),
            preserve_default=True,
        ),
    ]
