# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetnewssheet',
            name='equality_rights',
            field=models.CharField(help_text="Scan the full news story and code 'Yes' if it quotes or makes reference to any piece of legislation or policy that promotes gender equality or human rights.", max_length=1, verbose_name='Reference to gender equality / human rights legislation/ policy', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='equality_rights',
            field=models.CharField(help_text="Scan the full news story and code 'Yes' if it quotes or makes reference to any piece of legislation or policy that promotes gender equality or human rights.", max_length=1, verbose_name='Reference to gender equality / human rights legislation/ policy', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='equality_rights',
            field=models.CharField(help_text="Scan the full news story and code 'Yes' if it quotes or makes reference to any piece of legislation or policy that promotes gender equality or human rights.", max_length=1, verbose_name='Reference to gender equality / human rights legislation/ policy', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='equality_rights',
            field=models.CharField(help_text="Scan the full news story and code 'Yes' if it quotes or makes reference to any piece of legislation or policy that promotes gender equality or human rights.", max_length=1, verbose_name='Reference to gender equality / human rights legislation/ policy', choices=[(b'Y', 'Yes'), (b'N', 'No')]),
            preserve_default=True,
        ),
    ]
