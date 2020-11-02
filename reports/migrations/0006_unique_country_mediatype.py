# Generated by Django 2.2.18 on 2021-02-18 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_duplicate_weights'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='weights',
            constraint=models.UniqueConstraint(fields=('country', 'media_type'), name='country_media_type_key'),
        ),
    ]