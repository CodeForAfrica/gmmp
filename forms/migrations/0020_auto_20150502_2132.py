# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0019_auto_20150502_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetnewssheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor'),
            preserve_default=True,
        ),
    ]
