import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from gmmp.models import Monitor, GmmpUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Remove all users in the system
        GmmpUser.objects.all().delete()
        User.objects.filter(is_superuser=False).delete() # We don't want to delete superusers
        
        # Pull all gmmp users
        try:
            call_command('syncgsheets')
        except Exception:
            # TODO check why an exception is being raised despite all users being pulled
            pass

        gmmp_users = GmmpUser.objects.all()
        for gmmp_user in gmmp_users:
            # Create users
            group, _ = Group.objects.get_or_create(name=gmmp_user.Designation)
            user, _ = User.objects.get_or_create(email=gmmp_user.Email,
                        first_name=gmmp_user.Firstname, last_name=gmmp_user.Lastname, username=gmmp_user.Username)
            user.set_password(os.environ.get("SECRET_PASSWORD"))
            user.groups.add(group)

            # On sending activation email, user.is_staff should be set to true to enable user login
            user.save()
            monitor, _ = Monitor.objects.get_or_create(user=user)
            monitor.country = gmmp_user.Country
            monitor.save()
