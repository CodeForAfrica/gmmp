# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gmmp', '0001_initial'),
        ('forms', '0019_auto_20150506_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='internetnewssheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='internetnewssheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newspapersheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newspapersheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='radiosheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='radiosheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='televisionsheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='televisionsheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twittersheet',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twittersheet',
            name='monitor',
            field=models.ForeignKey(to='gmmp.Monitor', null=True),
            preserve_default=True,
        ),

        migrations.RunSQL(
            """
            update forms_internetnewssheet

            set country = monitor.country,
                monitor_id = monitor.id

            from
              forms_internetnewssheet as sheet
              inner join
                (select distinct object_pk, content_type_id, user_id from guardian_userobjectpermission) as perms on perms.object_pk = cast(sheet.id as varchar)
              inner join django_content_type on django_content_type.model = 'internetnewssheet' and perms.content_type_id = django_content_type.id
              inner join gmmp_monitor monitor on monitor.user_id = perms.user_id

            where forms_internetnewssheet.id = sheet.id
            ;

            update forms_newspapersheet

            set country = monitor.country,
                monitor_id = monitor.id

            from
              forms_newspapersheet as sheet
              inner join
                (select distinct object_pk, content_type_id, user_id from guardian_userobjectpermission) as perms on perms.object_pk = cast(sheet.id as varchar)
              inner join django_content_type on django_content_type.model = 'newspapersheet' and perms.content_type_id = django_content_type.id
              inner join gmmp_monitor monitor on monitor.user_id = perms.user_id

            where forms_newspapersheet.id = sheet.id
            ;

            update forms_televisionsheet

            set country = monitor.country,
                monitor_id = monitor.id

            from
              forms_televisionsheet as sheet
              inner join
                (select distinct object_pk, content_type_id, user_id from guardian_userobjectpermission) as perms on perms.object_pk = cast(sheet.id as varchar)
              inner join django_content_type on django_content_type.model = 'televisionsheet' and perms.content_type_id = django_content_type.id
              inner join gmmp_monitor monitor on monitor.user_id = perms.user_id

            where forms_televisionsheet.id = sheet.id
            ;

            update forms_radiosheet

            set country = monitor.country,
                monitor_id = monitor.id

            from
              forms_radiosheet as sheet
              inner join
                (select distinct object_pk, content_type_id, user_id from guardian_userobjectpermission) as perms on perms.object_pk = cast(sheet.id as varchar)
              inner join django_content_type on django_content_type.model = 'radiosheet' and perms.content_type_id = django_content_type.id
              inner join gmmp_monitor monitor on monitor.user_id = perms.user_id

            where forms_radiosheet.id = sheet.id
            ;

            update forms_twittersheet

            set country = monitor.country,
                monitor_id = monitor.id

            from
              forms_twittersheet as sheet
              inner join
                (select distinct object_pk, content_type_id, user_id from guardian_userobjectpermission) as perms on perms.object_pk = cast(sheet.id as varchar)
              inner join django_content_type on django_content_type.model = 'twittersheet' and perms.content_type_id = django_content_type.id
              inner join gmmp_monitor monitor on monitor.user_id = perms.user_id

            where forms_twittersheet.id = sheet.id
            ;
            """,
            """
            select 1;
            """
        )
    ]
