from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField
from gsheets.mixins import SheetPullableMixin


WEIGHT_TYPE = [
    ("R", _("Regional")),
    ("G", _("Global")),
]


class Weights(models.Model):
    country = CountryField()
    weight_type = models.CharField(choices=WEIGHT_TYPE, max_length=1, default="G")
    media_type = models.CharField(max_length=32)
    weight = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.country} {self.weight_type} {self.media_type} {self.weight}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "media_type", "weight_type"],
                name="country_media_weight_type_key",
            )
        ]


class GSheetGlobalCountryWeights(SheetPullableMixin, models.Model):
    spreadsheet_id = settings.GSHEETS_WEIGHTS["SPREADSHEET_ID"]
    sheet_name = settings.GSHEETS_WEIGHTS["GLOBAL_WEIGHTS_SHEET_NAME"]
    model_id_field = "guid"
    sheet_id_field = "Platform ID"

    guid = models.CharField(primary_key=True, max_length=255, default=uuid4)

    # NOTE(kilemensi): gsheets performs default insert for new rows before
    #                  doing an update with correct data. This means the model
    #                  must have valid default values for all fields.
    country = CountryField(default="KE")
    print_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    radio_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    television_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    internet_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    twitter_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.country} G: [{self.print_weight}, {self.radio_weight}, {self.television_weight}, {self.internet_weight}, {self.twitter_weight}]"

class GSheetRegionalCountryWeights(SheetPullableMixin, models.Model):
    spreadsheet_id = settings.GSHEETS_WEIGHTS["SPREADSHEET_ID"]
    sheet_name = settings.GSHEETS_WEIGHTS["REGIONAL_WEIGHTS_SHEET_NAME"]
    model_id_field = "guid"
    sheet_id_field = "Platform ID"

    guid = models.CharField(primary_key=True, max_length=255, default=uuid4)

    country = CountryField(default="KE")
    print_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    radio_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    television_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    internet_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    twitter_weight = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.country} R: [{self.print_weight}, {self.radio_weight}, {self.television_weight}, {self.internet_weight}, {self.twitter_weight}]"
