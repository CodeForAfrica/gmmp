# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0031_auto_20191212_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internetnewssheet',
            name='topic_comments',
        ),
        migrations.RemoveField(
            model_name='twittersheet',
            name='comments',
        ),
        migrations.AddField(
            model_name='internetnewsperson',
            name='special_qn_1',
            field=models.CharField(blank=True, max_length=1, verbose_name='(20) Special question 1', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='internetnewsperson',
            name='special_qn_2',
            field=models.CharField(blank=True, max_length=1, verbose_name='(21) Special question 2', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='internetnewsperson',
            name='special_qn_3',
            field=models.CharField(blank=True, max_length=1, verbose_name='(22) Special question 3', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='age',
            field=models.PositiveIntegerField(default=0, verbose_name='(10) Age (person appears)', choices=[(0, '(0) Do not know'), (1, '(1) 12 and under'), (2, '(2) 13-18'), (3, '(3) 19-34'), (4, '(4) 35-49'), (5, '(5) 50-64'), (6, '(6) 65 years or more')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='function',
            field=models.PositiveIntegerField(default=0, verbose_name='(12) Function in the news story', choices=[(0, '(0) Do not know'), (1, '(1) Subject'), (2, '(2) Spokesperson'), (3, '(3) Expert or commentator'), (4, '(4) Personal Experience'), (5, '(5) Eye Witness'), (6, '(6) Popular Opinion'), (7, '(7) Other')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='occupation',
            field=models.PositiveIntegerField(default=0, verbose_name='(11) Occupation or Position', choices=[(0, '(0) Not stated'), (1, '(1) Royalty, monarch, deposed monarch, etc.'), (2, '(2) Politician/ member of parliament, ...'), (3, '(3) Government employee, public servant, spokesperson, etc.'), (4, '(4) Police, military, para-military, militia, fire officer'), (5, '(5) Academic expert, lecturer, teacher'), (6, '(6) Doctor, dentist, health specialist'), (7, '(7) Health worker, social worker, childcare worker'), (8, '(8) Science/ technology professional, engineer, etc.'), (9, '(9) Media professional, journalist, film-maker, etc.'), (10, '(10) Lawyer, judge, magistrate, legal advocate, etc.'), (11, '(11) Business person, exec, manager, stock broker...'), (12, '(12) Office or service worker, non-management worker'), (13, '(13) Tradesperson, artisan, labourer, truck driver, etc.'), (14, '(14) Agriculture, mining, fishing, forestry'), (15, '(15) Religious figure, priest, monk, rabbi, mullah, nun'), (16, '(16) Activist or worker in civil society org., NGO, trade union'), (17, '(17) Sex worker'), (18, '(18) Celebrity, artist, actor, writer, singer, TV personality'), (19, '(19) Sportsperson, athlete, player, coach, referee'), (20, '(20) Student, pupil, schoolchild'), (21, '(21) Homemaker, parent (male or female)) only if no other occupation is given e.g. doctor/mother=code 6'), (22, '(22) Child, young person no other occupation given'), (23, '(23) Villager or resident no other occupation given'), (24, '(24) Retired person, pensioner no other occupation given'), (25, '(25) Criminal, suspect no other occupation given'), (26, '(26) Unemployed no other occupation given'), (27, '(27) Other only as last resort & explain')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='special_qn_1',
            field=models.CharField(blank=True, max_length=1, verbose_name='(14) Special question 1', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='special_qn_2',
            field=models.CharField(blank=True, max_length=1, verbose_name='(15) Special question 2', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='special_qn_3',
            field=models.CharField(blank=True, max_length=1, verbose_name='(16) Special question 3', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twittersheet',
            name='equality_rights',
            field=models.CharField(default=0, help_text="Scan the full news story and code 'Yes' if it quotes or makes reference to any piece of legislation or policy that promotes gender equality or human rights.", max_length=1, verbose_name='(3) Reference to gender equality / human rights legislation/ policy', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twittersheet',
            name='inequality_women',
            field=models.PositiveIntegerField(default=0, verbose_name='(5) This story clearly highlights issues of inequality between women and men', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='age',
            field=models.PositiveIntegerField(verbose_name='(13) Age (person appears)', choices=[(0, '(0) Do not know'), (1, '(1) 12 and under'), (2, '(2) 13-18'), (3, '(3) 19-34'), (4, '(4) 35-49'), (5, '(5) 50-64'), (6, '(6) 65 years or more')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='family_role',
            field=models.CharField(help_text="Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.", max_length=1, verbose_name='(16) Family Role Given?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='function',
            field=models.PositiveIntegerField(verbose_name='(15) Function in the news story', choices=[(0, '(0) Do not know'), (1, '(1) Subject'), (2, '(2) Spokesperson'), (3, '(3) Expert or commentator'), (4, '(4) Personal Experience'), (5, '(5) Eye Witness'), (6, '(6) Popular Opinion'), (7, '(7) Other')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='is_photograph',
            field=models.PositiveIntegerField(verbose_name='(21) Is there a photograph of the person in the story?', choices=[(1, '(1) Yes'), (2, '(2) No'), (3, '(3) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='is_quoted',
            field=models.CharField(help_text='<p>A person is <strong>directly quoted</strong> if their own words are printed, e.g. "The war against terror is our first priority" said President Bush.</p><p>If the story paraphrases what the person said, that is not a direct quote, e.g. President Bush said that top priority would be given to fighting the war against terror.</p>', max_length=1, verbose_name='(20) Is the person directly quoted', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='occupation',
            field=models.PositiveIntegerField(verbose_name='(14) Occupation or Position', choices=[(0, '(0) Not stated'), (1, '(1) Royalty, monarch, deposed monarch, etc.'), (2, '(2) Politician/ member of parliament, ...'), (3, '(3) Government employee, public servant, spokesperson, etc.'), (4, '(4) Police, military, para-military, militia, fire officer'), (5, '(5) Academic expert, lecturer, teacher'), (6, '(6) Doctor, dentist, health specialist'), (7, '(7) Health worker, social worker, childcare worker'), (8, '(8) Science/ technology professional, engineer, etc.'), (9, '(9) Media professional, journalist, film-maker, etc.'), (10, '(10) Lawyer, judge, magistrate, legal advocate, etc.'), (11, '(11) Business person, exec, manager, stock broker...'), (12, '(12) Office or service worker, non-management worker'), (13, '(13) Tradesperson, artisan, labourer, truck driver, etc.'), (14, '(14) Agriculture, mining, fishing, forestry'), (15, '(15) Religious figure, priest, monk, rabbi, mullah, nun'), (16, '(16) Activist or worker in civil society org., NGO, trade union'), (17, '(17) Sex worker'), (18, '(18) Celebrity, artist, actor, writer, singer, TV personality'), (19, '(19) Sportsperson, athlete, player, coach, referee'), (20, '(20) Student, pupil, schoolchild'), (21, '(21) Homemaker, parent (male or female)) only if no other occupation is given e.g. doctor/mother=code 6'), (22, '(22) Child, young person no other occupation given'), (23, '(23) Villager or resident no other occupation given'), (24, '(24) Retired person, pensioner no other occupation given'), (25, '(25) Criminal, suspect no other occupation given'), (26, '(26) Unemployed no other occupation given'), (27, '(27) Other only as last resort & explain')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='sex',
            field=models.PositiveIntegerField(verbose_name='(12) Sex', choices=[(1, '(1) Female'), (2, '(2) Male'), (3, '(3) Other (transgender, etc.)'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='survivor_of',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='(19) The story identifies the person as a survivor of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a victim)'), (1, '(1) Survivor of an accident, natural disaster, poverty'), (2, '(2) Survivor of domestic violence, rape, murder, etc.'), (3, '(3) Survivor of non-domestic sexual violence, rape, assault, etc. (sexual violence only)'), (4, '(4) Survivor of other non-domestic crime, robbery, etc.'), (5, '(5) Survivor of violation based on religion, tradition...'), (6, '(6) Survivor of war, terrorism, vigilantism, state violence...'), (7, '(7) Survivor of discrimination based on gender, race, ethnicity, age, religion, ability, etc.'), (8, '(8) Other survivor (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='victim_of',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='(18) The story identifies the person as a victim of:', choices=[(0, '(0) Not applicable (the story identifies the person only as a survivor)'), (1, '(1) Victim of an accident, natural disaster, poverty'), (2, '(2) Victim of domestic violence, rape, murder, etc.'), (3, '(3) Victim of non-domestic sexual violence, rape, assault, etc (sexual violence only)'), (4, '(4) Victim of other non-domestic crime, robbery, etc.'), (5, '(5) Victim of violation based on religion, tradition...'), (6, '(6) Victim of war, terrorism, vigilantism, state violence...'), (7, '(7) Victim of discrimination based on gender, race, ethnicity, age, religion, ability, etc'), (8, '(8) Other victim (specify in comments)'), (9, '(9) Do not know, cannot decide')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewsperson',
            name='victim_or_survivor',
            field=models.CharField(help_text="<p>You should code a person as a <strong>victim</strong> either if the word 'victim' is used to describe her/him, or if the story Implies that the person is a victim - e.g. by using language or images that evoke particular emotions such as shock, horror, pity for the person.</p><p>You should code a person as a <strong>survivor</strong> either if the word 'survivor' is used to describe her/him, or if the story implies that the person is a survivor - e.g. by using language or images that evoke particular emotions such as admiration or respect for the person.</p>", max_length=1, verbose_name='(17) Does the story identify the person as either a victim or survivor?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='about_women',
            field=models.CharField(max_length=1, verbose_name='(7) Is the story about a particular woman or group of women?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='further_analysis',
            field=models.CharField(help_text="<br><br>A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation", max_length=1, verbose_name='(26) Does this story warrant further analysis?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='inequality_women',
            field=models.PositiveIntegerField(verbose_name='(8) This story clearly highlights issues of inequality between women and men', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='shared_via_twitter',
            field=models.CharField(help_text='Has this story been shared by the media house via Twitter?\n\n<br>Enter the exact URL of the story into <a href="https://unionmetrics.com/free-tools/twitter-snapshot-report/" target="_blank">https://unionmetrics.com/free-tools/twitter-snapshot-report/</a> - answer yes if the media house\'s name appears in the search results.', max_length=1, verbose_name='(4) Shared via twitter?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(9) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='url_and_multimedia',
            field=models.TextField(verbose_name='(25) Copy and paste the URL of the story. Describe any photographs, images, other multimedia features included in the story. Note down the conclusions you draw from the images, audio and video.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twitterperson',
            name='is_photograph',
            field=models.PositiveIntegerField(verbose_name='(13) Is there a photograph of the person in the story?', choices=[(1, '(1) Yes'), (2, '(2) No'), (3, '(3) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twitterperson',
            name='sex',
            field=models.PositiveIntegerField(verbose_name='(9) Sex', choices=[(1, '(1) Female'), (2, '(2) Male'), (3, '(3) Other (transgender, etc.)'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='about_women',
            field=models.CharField(max_length=1, verbose_name='(4) Is the story about a particular woman or group of women?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='further_analysis',
            field=models.CharField(help_text="<br><br>A tweet warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation", max_length=1, verbose_name='(18) Does this tweet warrant further analysis?', choices=[(b'Y', '(1) Yes'), (b'N', '(2) No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='stereotypes',
            field=models.PositiveIntegerField(help_text='This story clearly challenges gender stereotypes', verbose_name='(6) Challenges Stereotypes', choices=[(1, '(1) Agree'), (2, '(2) Disagree'), (3, '(3) Neither agree nor disagree'), (4, '(4) Do not know')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='twitter_handle',
            field=models.CharField(help_text='e.g. @cnnbrk', max_length=255, verbose_name='Twitter Handle'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='twittersheet',
            name='url_and_multimedia',
            field=models.TextField(verbose_name='(17) Copy and paste the URL of the tweet. Describe any photographs, images, other multimedia features included in the tweet. Note down the conclusions you draw from the images, audio and video.', blank=True),
            preserve_default=True,
        ),
    ]
