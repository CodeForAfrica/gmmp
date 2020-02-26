# Generated by Django 2.2.9 on 2020-02-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0043_update_country_region'),
    ]

    operations = [
        migrations.RenameField(
            model_name='televisionsheet',
            old_name='television_channel',
            new_name='channel',
        ),
        migrations.RemoveField(
            model_name='televisionsheet',
            name='station_name',
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='shared_on_facebook',
            field=models.CharField(choices=[('Y', '(1) Yes'), ('N', '(2) No')], help_text="Has this story been shared by the media house on its Facebook Page?\n\n<br>Scroll down the media house's Facebook page to check.", max_length=1, verbose_name='(5) Shared on Facebook'),
        ),
        migrations.AlterField(
            model_name='internetnewssheet',
            name='shared_via_twitter',
            field=models.CharField(choices=[('Y', '(1) Yes'), ('N', '(2) No')], help_text='Has this story been shared by the media house via Twitter?\n\n<br>Enter the exact URL of the story into <a href="https://twitter.com" target="_blank">https://twitter.com</a> - answer yes if the media house\'s name appears in the search results.', max_length=1, verbose_name='(4) Shared via twitter?'),
        ),
        migrations.AlterField(
            model_name='radiosheet',
            name='station_name',
            field=models.CharField(help_text="Be as specific as possible. E.g. if the radio company is called RRI, and if the newscast is broadcast on its third channel, write in 'RRI-3'.", max_length=255, verbose_name='Channel'),
        ),
        migrations.RenameField(
            model_name='radiosheet',
            old_name='station_name',
            new_name='channel',
        ),
    ]
