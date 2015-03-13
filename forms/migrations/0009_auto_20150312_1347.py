# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0008_auto_20150309_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internetnewssheet',
            name='comments',
        ),
        migrations.AddField(
            model_name='radiosheet',
            name='comments',
            field=models.TextField(verbose_name='Describe any photographs included in the story and the conclusions you draw from them.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='family_role',
            field=models.CharField(help_text="Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.", max_length=1, verbose_name='Family Role Given?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='family_role',
            field=models.CharField(help_text="Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.", max_length=1, verbose_name='Family Role Given?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radioperson',
            name='family_role',
            field=models.CharField(help_text="Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.", max_length=1, verbose_name='Family Role Given?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionperson',
            name='family_role',
            field=models.CharField(help_text="Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.", max_length=1, verbose_name='Family Role Given?', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
    ]
