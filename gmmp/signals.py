from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(pre_save, sender=User)
def ensure_staff(sender, instance, signal, **kwargs):
    instance.is_staff = True

@receiver(post_save, sender=User)
def create_admin_group(sender, instance, signal, created, **kwargs):
    if instance.monitor.country != None:
        country = instance.monitor.country
        Group.objects.get_or_create(name='%s_admin' % country)
