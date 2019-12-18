# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0029_auto_20191210_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newspaperperson',
            name='special_qn_1',
            field=models.CharField(blank=True, max_length=1, verbose_name='(20) Special question 1', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='special_qn_2',
            field=models.CharField(blank=True, max_length=1, verbose_name='(21) Special question 2', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='special_qn_3',
            field=models.CharField(blank=True, max_length=1, verbose_name='(22) Special question 3', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
    ]
