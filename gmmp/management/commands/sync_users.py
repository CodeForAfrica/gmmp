import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.conf import settings
from gmmp.models import Monitor, CountryUser

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Remove all users in the system
        CountryUser.objects.all().delete()
        User.objects.filter(is_superuser=False).delete() # We don't want to delete superusers
        
        # Pull all gmmp users
        try:
            call_command('syncgsheets')
        except Exception:
            # TODO check why an exception is being raised despite all users being pulled
            pass

        country_users = CountryUser.objects.all()
        for country_user in country_users:
            # Create users
            group, _ = Group.objects.get_or_create(name=country_user.Designation)
            user, _ = User.objects.get_or_create(email=country_user.Email,
                        first_name=country_user.Firstname, last_name=country_user.Lastname, username=country_user.Username)
            user.set_password(settings.COUNTRY_USER_DEFAULT_PASSWORD)
            user.groups.add(group)

            # On sending activation email, user.is_staff should be set to true to enable user login
            user.save()
            monitor, _ = Monitor.objects.get_or_create(user=user)
            monitor.country = country_user.Country
            monitor.save()
