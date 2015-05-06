from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import signals

class Monitor(models.Model):
    user = models.OneToOneField(User)
    country = CountryField()

    def __unicode__(self):
        return "%s" % self.country


