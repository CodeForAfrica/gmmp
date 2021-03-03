from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from django_countries import countries
from gsheets.signals import sheet_row_processed

from .models import Weights, GSheetCountryWeights


@receiver(sheet_row_processed, sender=GSheetCountryWeights)
def update_or_create_weights_from_gsheetweights(
    instance=None, created=None, row_data=None, **kwargs
):
    try:
        country = countries.alpha2(row_data["Country"])
        print_weight = row_data["Print"]
        radio_weight = row_data["Radio"]
        television_weight = row_data["Television"]
        internet_weight = row_data["Internet"]
        twitter_weight = row_data["Twitter"]
        Weights.objects.update_or_create(
            country=country, media_type="Print", defaults={"weight": print_weight}
        )
        Weights.objects.update_or_create(
            country=country, media_type="Radio", defaults={"weight": radio_weight}
        )
        Weights.objects.update_or_create(
            country=country,
            media_type="Television",
            defaults={"weight": television_weight},
        )
        Weights.objects.update_or_create(
            country=country, media_type="Internet", defaults={"weight": internet_weight}
        )
        Weights.objects.update_or_create(
            country=country, media_type="Twitter", defaults={"weight": twitter_weight}
        )
        instance.country = country
        instance.print_weight = print_weight
        instance.radio_weight = radio_weight
        instance.tv_weight = television_weight
        instance.internet_weight = internet_weight
        instance.twitter_weight = twitter_weight
        instance.save()
    except (ObjectDoesNotExist, KeyError):
        pass
