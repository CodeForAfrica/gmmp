from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django_countries.fields import countries
from gsheets.signals import sheet_row_processed
from .models import Monitor, SpecialQuestions, CountryUser

@receiver(post_save, sender=User)
def create_admin_group(sender, instance, signal, created, **kwargs):
    try:
        monitor = instance.monitor
    except:
        monitor, created = Monitor.objects.get_or_create(user=instance)
        monitor.save()
        Group.objects.get_or_create(name='%s_admin' % monitor.country)

@receiver(sheet_row_processed, sender=SpecialQuestions)
def match_special_questions_columns_to_fields(instance=None, created=None, row_data=None, **kwargs):
    try:
        instance.country = countries.alpha2(row_data['Country'])
        instance.question_1 = row_data['Question 1'].strip()
        instance.question_2 = row_data['Question 2'].strip()
        instance.question_3 = row_data['Question 3'].strip()
        instance.save()
    except (ObjectDoesNotExist, KeyError):
        pass

@receiver(sheet_row_processed, sender=CountryUser)
def match_country_users_columns_to_fields(instance=None, created=None, row_data=None, **kwargs):
    try:
        instance.country = countries.alpha2(row_data['Country'])
        instance.firstname = row_data['Firstname'].strip()
        instance.lastname = row_data['Lastname'].strip()
        instance.username = row_data['Username'].strip()
        instance.email = row_data['Email'].strip()
        instance.designation = row_data['Designation'].strip()
        instance.save()
    except (ObjectDoesNotExist, KeyError):
        pass
