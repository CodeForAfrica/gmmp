# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0005_internetnewsperson_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='internetnewsperson',
            name='is_photograph',
            field=models.PositiveIntegerField(default=None, verbose_name='Is there a photograph of the person in the story?', choices=[(1, 'Yes'), (2, 'No'), (3, 'Do not know')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internetnewsperson',
            name='is_quoted',
            field=models.CharField(default=None, help_text='<p>A person is <strong>directly quoted</strong> if their own words are printed, e.g. "The war against terror is our first priority" said President Bush.</p><p>If the story paraphrases what the person said, that is not a direct quote, e.g. President Bush said that top priority would be given to fighting the war against terror.</p>', max_length=1, verbose_name='Is the person directly quoted', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=False,
        ),
    ]
