from django.db import models
from django.contrib.auth.models import User

class Monitor(models.Model):
    user = models.OneToOneField(User)
    country = models.CharField(max_length=100)


