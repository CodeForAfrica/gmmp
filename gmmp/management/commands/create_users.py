import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from gmmp.models import Monitor


class Command(BaseCommand):
    def handle(self, *args, **options):
        SHEET_KEY = os.environ.get("SHEET_KEY")
        GOOGLE_CREDENTIALS = json.loads(os.environ.get("GOOGLE_CREDENTIALS", '{}'))
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive",]

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_CREDENTIALS, scopes=scope)

        client = gspread.authorize(credentials)

        sheet = client.open_by_key(SHEET_KEY)
        worksheet = sheet.worksheet('data')

        records = worksheet.get_all_records()

        for record in records:
            # Create users
            email = record.get('Email')
            first_name = record.get('Firstname')
            last_name = record.get('Lastname')
            username = record.get('Username')
            country = record.get('Country')
            group, _ = Group.objects.get_or_create(name=record.get('Designation'))
            user, _ = User.objects.get_or_create(email=email, first_name=first_name, last_name=last_name, username=username)
            user.set_password("RandomPassword321")
            user.groups.add(group)

            user.is_staff = True
            user.save()
    
            monitor, _ = Monitor.objects.get_or_create(user=user)
            monitor.country = country
            monitor.save()

