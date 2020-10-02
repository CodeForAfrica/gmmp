# Generated by Django 2.2.16 on 2020-10-01 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0057_add_monitor_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='internetnewsjournalist',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this Journalist as deleted.'),
        ),
        migrations.AddField(
            model_name='internetnewsperson',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this person as deleted.'),
        ),
        migrations.AddField(
            model_name='internetnewssheet',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this sheet as deleted.'),
        ),
        migrations.AddField(
            model_name='newspaperjournalist',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this Journalist as deleted.'),
        ),
        migrations.AddField(
            model_name='newspaperperson',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this person as deleted.'),
        ),
        migrations.AddField(
            model_name='newspapersheet',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this sheet as deleted.'),
        ),
        migrations.AddField(
            model_name='radiojournalist',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this Journalist as deleted.'),
        ),
        migrations.AddField(
            model_name='radioperson',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this person as deleted.'),
        ),
        migrations.AddField(
            model_name='radiosheet',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this sheet as deleted.'),
        ),
        migrations.AddField(
            model_name='televisionjournalist',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this Journalist as deleted.'),
        ),
        migrations.AddField(
            model_name='televisionperson',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this person as deleted.'),
        ),
        migrations.AddField(
            model_name='televisionsheet',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this sheet as deleted.'),
        ),
        migrations.AddField(
            model_name='twitterjournalist',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this Journalist as deleted.'),
        ),
        migrations.AddField(
            model_name='twitterperson',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this person as deleted.'),
        ),
        migrations.AddField(
            model_name='twittersheet',
            name='deleted',
            field=models.BooleanField(default=False, help_text='Mark this sheet as deleted.'),
        ),
    ]
