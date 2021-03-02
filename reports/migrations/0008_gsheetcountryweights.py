# Generated by Django 2.2.18 on 2021-03-01 21:07

from django.db import migrations, models
import django_countries.fields
import gsheets.mixins
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0007_proxy_weights'),
    ]

    operations = [
        migrations.CreateModel(
            name='GSheetCountryWeights',
            fields=[
                ('guid', models.CharField(default=uuid.uuid4, max_length=255, primary_key=True, serialize=False)),
                ('country', django_countries.fields.CountryField(default='KE', max_length=2)),
                ('print_weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('radio_weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('tv_weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('internet_weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('twitter_weight', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
            ],
            bases=(gsheets.mixins.SheetPullableMixin, models.Model),
        ),
    ]
