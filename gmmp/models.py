from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class Monitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(default='KE')

    def __unicode__(self):
        return "%s" % self.country


class SpecialQuestions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(default='KE')
    question_1 = models.TextField()
    question_2 = models.TextField()
    question_3 = models.TextField()

    def __str__(self):
        return f"{self.user.monitor.country} special questions"
