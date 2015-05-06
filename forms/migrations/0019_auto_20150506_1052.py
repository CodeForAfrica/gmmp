# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0018_auto_20150416_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetnewssheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(23) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='space',
            field=models.PositiveIntegerField(verbose_name='(4) Space', choices=[(1, '(1) Full page'), (2, '(2) Half page'), (3, '(3) One third page'), (4, '(4) Quarter page'), (5, '(5) Less than quarter page')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(21) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiojournalist',
            name='role',
            field=models.PositiveIntegerField(verbose_name='Role', choices=[(1, '(1) Anchor, announcer or presenter: Usually in the television studio'), (2, '(2) Reporter: Usually outside the studio. Include reporters who do not appear on screen, but whose voice is heard (e.g. as voice-over).'), (3, '(3) Other journalist: Sportscaster, weather forecaster, commentator/analyst etc.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(16) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionjournalist',
            name='role',
            field=models.PositiveIntegerField(verbose_name='Role', choices=[(1, '(1) Anchor, announcer or presenter: Usually in the television studio'), (2, '(2) Reporter: Usually outside the studio. Include reporters who do not appear on screen, but whose voice is heard (e.g. as voice-over).'), (3, '(3) Other journalist: Sportscaster, weather forecaster, commentator/analyst etc.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(18) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This tweet clearly challenges gender stereotypes', verbose_name='(8) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
    ]
