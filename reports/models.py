from django.db import models
from django_countries.fields import CountryField


class Weights(models.Model):
    country = CountryField()
    media_type = models.CharField(max_length=32)
    weight = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.country} {self.media_type} {self.weight}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "media_type"], name="country_media_type_key"
            )
        ]
