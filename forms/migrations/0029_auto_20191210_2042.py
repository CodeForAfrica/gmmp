# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0028_auto_20191210_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspaperperson',
            name='special_qn_1',
            field=models.CharField(blank=True, max_length=1, verbose_name='(20) Special Question 1', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='special_qn_2',
            field=models.CharField(blank=True, max_length=1, verbose_name='(21) Special Question 2', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='special_qn_3',
            field=models.CharField(blank=True, max_length=1, verbose_name='(22) Special Question 3', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
    ]
