from django.core.management.base import BaseCommand
from django.db.models import F
from sheets.data_transfer.data_upload import DataUpload

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Sheet transfer starting")
        DataUpload().post()
        self.stdout.write("Sheet transfer completed")
