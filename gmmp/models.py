from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Monitor(models.Model):
    user = models.OneToOneField(User)
    country = CountryField()


