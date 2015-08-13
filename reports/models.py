from django.db import models
from django_countries.fields import CountryField


class Weights(models.Model):
  country = CountryField()
  media_type = models.CharField(max_length=32)
  weight = models.DecimalField(max_digits=4, decimal_places=2)
