# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0024_auto_20191210_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspapersheet',
            name='person_secondary',
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='comments',
            field=models.TextField(verbose_name='(23) Describe any photographs included in the story and the conclusions you draw from them.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='further_analysis',
            field=models.CharField(help_text="<br><br>A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation", max_length=1, verbose_name='(24) Does this story warrant further analysis?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='inequality_women',
            field=models.PositiveIntegerField(verbose_name='(7) This story clearly highlights issues of inequality between women and men', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(8) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
    ]
