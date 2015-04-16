# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0017_auto_20150331_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetnewssheet',
            name='webpage_layer_no',
            field=models.PositiveIntegerField(help_text='Webpage Layer Number. Homepage=1, One click away=2, Five clicks away= 5, etc. Note that if a story appears on the front page, code with 1', verbose_name='(1) Webpage Layer Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='page_number',
            field=models.PositiveIntegerField(help_text='Write in the number of the page on which the story begins. Story appears on first page = 1, Seventh page = 7, etc.', verbose_name='(1) Page Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='item_number',
            field=models.PositiveIntegerField(help_text='Write in the number that describes the position of the story within the newscast. E.g. the first story in the newscast is item 1; the seventh story is item 7.', verbose_name='(1) Item Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='num_female_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other', verbose_name='Number of female anchors'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='num_male_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other journalists</strong>', verbose_name='Number of male anchors'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='item_number',
            field=models.PositiveIntegerField(help_text='Write in the number that describes the position of the story within the newscast. E.g. the first story in the newscast is item 1; the seventh story is item 7.', verbose_name='(1) Item Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='num_female_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other', verbose_name='Number of female anchors'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='num_male_anchors',
            field=models.PositiveIntegerField(help_text='The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other journalists</strong>', verbose_name='Number of male anchors'),
            preserve_default=True,
        ),
    ]
