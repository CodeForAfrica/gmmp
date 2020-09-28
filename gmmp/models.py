from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from gsheets.mixins import SheetPullableMixin
from uuid import uuid4

class Monitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(default='KE')

    def __unicode__(self):
        return "%s" % self.country

class SpecialQuestions(SheetPullableMixin, models.Model):
    spreadsheet_id = settings.GSHEETS_SPECIAL_QUESTIONS['SPREADSHEET_ID']
    sheet_name = settings.GSHEETS_SPECIAL_QUESTIONS['SHEET_NAME']
    model_id_field = 'guid'
    sheet_id_field = 'Platform ID'

    guid = models.CharField(primary_key=True, max_length=255, default=uuid4)
        
    country = CountryField(default='KE')
    question_1 = models.TextField()
    question_2 = models.TextField()
    question_3 = models.TextField()

    def __str__(self):
        return f"{self.country} Special Questions"

class CountryUser(SheetPullableMixin, models.Model):
    spreadsheet_id = settings.GSHEET_COUNTRY_USERS['SPREADSHEET_ID']
    sheet_name = settings.GSHEET_COUNTRY_USERS['SHEET_NAME']
    
    guid = models.CharField(primary_key=True, max_length=255, default=uuid4)
    
    Country = models.CharField(max_length=127)
    Firstname = models.CharField(max_length=127)
    Lastname = models.CharField(max_length=127)
    Username = models.CharField(max_length=127)
    Email = models.CharField(max_length=127)
    Designation = models.CharField(max_length=127)
