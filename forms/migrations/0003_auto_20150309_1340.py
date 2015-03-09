# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_auto_20150309_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='televisionsheet',
            name='person_secondary',
            field=models.PositiveIntegerField(default=None, help_text="<br><br>\n    Select ''Secondary Source'' only if the story is based solely on information from a report, article, or other piece of written information.<br><br>\n<strong>Code information for:</strong><br>\n  - Any person whom the story is about even if they are not interviewed or quoted<br>\n  - Each person who is interviewed<br>\n  - Each person in the story who is quoted, either directly or indirectly. Code only individual people.<br>\n<br>\n<strong>Do not code:</strong>\n  - Groups (e.g. a group of nurses, a group of soldiers);</br>\n  - Organisations, companies, collectivities (e.g. political parties);</br>\n  - Characters in novels or movies (unless the story is about them);</br>\n  - Deceased historical figures (unless the story is about them);</br>\n  - Interpreters (Code the person being interviewed as if they spoke without an interpreter).</br>\n", verbose_name='Source', choices=[(1, 'Person'), (2, 'Secondary Source')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='num_female_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other', verbose_name='Number of female anchors', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='num_male_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other journalists</strong>', verbose_name='Number of male anchors', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='num_female_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other', verbose_name='Number of female anchors', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='num_male_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other journalists</strong>', verbose_name='Number of male anchors', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]),
            preserve_default=True,
        ),
    ]
