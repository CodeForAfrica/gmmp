# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0014_auto_20150325_0747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetnewsperson',
            name='is_photograph',
            field=models.PositiveIntegerField(verbose_name='(19) Is there a photograph of the person in the story?', choices=[(1, '(1) Yes'), (2, '(2) No'), (3, '(3) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='survivor_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(17) The story identifies the person as a survivor of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a victim)'), (1, '(1) Survivor of an accident, natural disaster, poverty'), (2, '(2) Survivor of domestic violence, rape, murder, etc.'), (3, '(3) Survivor of non-domestic sexual violence, rape, assault, etc. (sexual violence only)'), (4, '(4) Survivor of other non-domestic crime, robbery, etc.'), (5, '(5) Survivor of violation based on religion, tradition...'), (6, '(6) Survivor of war, terrorism, vigilantism, state violence...'), (7, '(7) Survivor of discrimination based on gender, race, ethnicity, age, religion, ability, etc.'), (8, '(8) Other survivor (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='victim_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(16) The story identifies the person as a victim of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a survivor)'), (1, '(1) Victim of an accident, natural disaster, poverty'), (2, '(2) Victim of domestic violence, rape, murder, etc.'), (3, '(3) Victim of non-domestic sexual violence, rape, assault, etc (sexual violence only)'), (4, '(4) Victim of other non-domestic crime, robbery, etc.'), (5, '(5) Victim of violation based on religion, tradition...'), (6, '(6) Victim of war, terrorism, vigilantism, state violence...'), (7, '(7) Victim of discrimination based on gender, race, ethnicity, age, religion, ability, etc'), (8, '(8) Other victim (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='inequality_women',
            field=models.PositiveIntegerField(verbose_name='(22) This story clearly highlights issues of inequality between women and men', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(23) Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='is_photograph',
            field=models.PositiveIntegerField(verbose_name='(17) Is there a photograph of the person in the story?', choices=[(1, '(1) Yes'), (2, '(2) No'), (3, '(3) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='survivor_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(15) The story identifies the person as a survivor of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a victim)'), (1, '(1) Survivor of an accident, natural disaster, poverty'), (2, '(2) Survivor of domestic violence, rape, murder, etc.'), (3, '(3) Survivor of non-domestic sexual violence, rape, assault, etc. (sexual violence only)'), (4, '(4) Survivor of other non-domestic crime, robbery, etc.'), (5, '(5) Survivor of violation based on religion, tradition...'), (6, '(6) Survivor of war, terrorism, vigilantism, state violence...'), (7, '(7) Survivor of discrimination based on gender, race, ethnicity, age, religion, ability, etc.'), (8, '(8) Other survivor (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspaperperson',
            name='victim_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(14) The story identifies the person as a victim of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a survivor)'), (1, '(1) Victim of an accident, natural disaster, poverty'), (2, '(2) Victim of domestic violence, rape, murder, etc.'), (3, '(3) Victim of non-domestic sexual violence, rape, assault, etc (sexual violence only)'), (4, '(4) Victim of other non-domestic crime, robbery, etc.'), (5, '(5) Victim of violation based on religion, tradition...'), (6, '(6) Victim of war, terrorism, vigilantism, state violence...'), (7, '(7) Victim of discrimination based on gender, race, ethnicity, age, religion, ability, etc'), (8, '(8) Other victim (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='inequality_women',
            field=models.PositiveIntegerField(verbose_name='(20) This story clearly highlights issues of inequality between women and men', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newspapersheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(21) Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radioperson',
            name='survivor_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(13) The story identifies the person as a survivor of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a victim)'), (1, '(1) Survivor of an accident, natural disaster, poverty'), (2, '(2) Survivor of domestic violence, rape, murder, etc.'), (3, '(3) Survivor of non-domestic sexual violence, rape, assault, etc. (sexual violence only)'), (4, '(4) Survivor of other non-domestic crime, robbery, etc.'), (5, '(5) Survivor of violation based on religion, tradition...'), (6, '(6) Survivor of war, terrorism, vigilantism, state violence...'), (7, '(7) Survivor of discrimination based on gender, race, ethnicity, age, religion, ability, etc.'), (8, '(8) Other survivor (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radioperson',
            name='victim_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(12) The story identifies the person as a victim of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a survivor)'), (1, '(1) Victim of an accident, natural disaster, poverty'), (2, '(2) Victim of domestic violence, rape, murder, etc.'), (3, '(3) Victim of non-domestic sexual violence, rape, assault, etc (sexual violence only)'), (4, '(4) Victim of other non-domestic crime, robbery, etc.'), (5, '(5) Victim of violation based on religion, tradition...'), (6, '(6) Victim of war, terrorism, vigilantism, state violence...'), (7, '(7) Victim of discrimination based on gender, race, ethnicity, age, religion, ability, etc'), (8, '(8) Other victim (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='inequality_women',
            field=models.PositiveIntegerField(verbose_name='(15) This story clearly highlights issues of inequality between women and men', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(16) Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionperson',
            name='survivor_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(15) The story identifies the person as a survivor of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a victim)'), (1, '(1) Survivor of an accident, natural disaster, poverty'), (2, '(2) Survivor of domestic violence, rape, murder, etc.'), (3, '(3) Survivor of non-domestic sexual violence, rape, assault, etc. (sexual violence only)'), (4, '(4) Survivor of other non-domestic crime, robbery, etc.'), (5, '(5) Survivor of violation based on religion, tradition...'), (6, '(6) Survivor of war, terrorism, vigilantism, state violence...'), (7, '(7) Survivor of discrimination based on gender, race, ethnicity, age, religion, ability, etc.'), (8, '(8) Other survivor (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionperson',
            name='victim_of',
            field=models.PositiveIntegerField(null=True, verbose_name='(14) The story identifies the person as a victim of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a survivor)'), (1, '(1) Victim of an accident, natural disaster, poverty'), (2, '(2) Victim of domestic violence, rape, murder, etc.'), (3, '(3) Victim of non-domestic sexual violence, rape, assault, etc (sexual violence only)'), (4, '(4) Victim of other non-domestic crime, robbery, etc.'), (5, '(5) Victim of violation based on religion, tradition...'), (6, '(6) Victim of war, terrorism, vigilantism, state violence...'), (7, '(7) Victim of discrimination based on gender, race, ethnicity, age, religion, ability, etc'), (8, '(8) Other victim (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='inequality_women',
            field=models.PositiveIntegerField(verbose_name='(17) This story clearly highlights issues of inequality between women and men', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='televisionsheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(18) Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twitterperson',
            name='is_photograph',
            field=models.PositiveIntegerField(verbose_name='(5) Is there a photograph of the person in the story?', choices=[(1, '(1) Yes'), (2, '(2) No'), (3, '(3) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='retweet',
            field=models.PositiveIntegerField(help_text='Only retweets from the same media house can be coded. Do not code retweets from other news providers', verbose_name='(1) Tweet or Retweet', choices=[(1, '(1) Tweet'), (2, '(2) Retweet')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This tweet clearly challenges gender stereotypes', verbose_name='(8) Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
    ]
