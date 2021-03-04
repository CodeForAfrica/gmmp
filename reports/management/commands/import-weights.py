from django.core.management.base import BaseCommand

from reports.models import GSheetGlobalCountryWeights, GSheetRegionalCountryWeights


class Command(BaseCommand):
    help = "Import weights from a gSheet and update DB"

    def handle(self, *args, **options):
        # NOTE(kilemensi): Don't call `syncgsheets` since it auto discovers
        #                  and sync **all** models
        GSheetGlobalCountryWeights.pull_sheet()
        GSheetRegionalCountryWeights.pull_sheet()
