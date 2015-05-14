from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.contrib import admin

from gmmp.models import Monitor
from forms.admin import (
    RadioSheetAdmin, TwitterSheetAdmin, InternetNewsSheetAdmin,
    NewspaperSheetAdmin, TelevisionSheetAdmin)

from forms.models import (
    RadioSheet, TwitterSheet, InternetNewsSheet, NewspaperSheet,
    TelevisionSheet)

from sheets import (radio_sheets, twitter_sheets, internetnews_sheets,
    newspaper_sheets, television_sheets)


sheet_types = [
    (RadioSheet, RadioSheetAdmin, radio_sheets),
    (TwitterSheet, TwitterSheetAdmin, twitter_sheets),
    (InternetnewsSheet, InternetNewsSheetAdmin, internetnews_sheets),
    (NewspaperSheet, NewspaperSheetAdmin, newspaper_sheets),
    (TelevisionSheet, TelevisionSheetAdmin, television_sheets)
]

class Command(BaseCommand):

    def handle(self, *args, **options):

        for model, model_admin, sheet_monitor_list in sheet_types:
            admin_obj =model_admin(model, admin.site)

            for sheet_id, monitor_id in sheet_monitor_list:
                user = User.objects.get(monitor__id=monitor_id)
                sheet_obj = model.objects.get(id=sheet_id)

                admin_obj.assign_permissions(user, sheet_obj)
