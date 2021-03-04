from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver

from django_countries import countries
from gsheets.signals import sheet_row_processed

from forms.modelutils import MEDIA_TYPES

from .models import Weights, GSheetGlobalCountryWeights, GSheetRegionalCountryWeights


def _update_or_create_weights_from_gsheetcountryweights(
    weight_type, instance, row_data
):
    country = countries.alpha2(row_data["Country"])
    instance.country = country

    for _, media_type in MEDIA_TYPES:
        weight = row_data[media_type]
        Weights.objects.update_or_create(
            country=country,
            weight_type=weight_type,
            media_type=media_type,
            defaults={"weight": weight},
        )
        media_weight_attr_name = f"{media_type.lower()}_weight"
        setattr(instance, media_weight_attr_name, weight)

    instance.save()


@receiver(sheet_row_processed, sender=GSheetGlobalCountryWeights)
def update_or_create_weights_from_gsheetglobalcountryweights(
    instance=None, created=None, row_data=None, **kwargs
):
    try:
        _update_or_create_weights_from_gsheetcountryweights("G", instance, row_data)
    except (ObjectDoesNotExist, KeyError):
        pass


@receiver(sheet_row_processed, sender=GSheetRegionalCountryWeights)
def update_or_create_weights_from_gsheetregionalcountryweights(
    instance=None, created=None, row_data=None, **kwargs
):
    try:
        _update_or_create_weights_from_gsheetcountryweights("R", instance, row_data)
    except (ObjectDoesNotExist, KeyError):
        pass
