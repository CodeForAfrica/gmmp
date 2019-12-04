from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Monitor

@receiver(post_save, sender=User)
def create_admin_group(sender, instance, signal, created, **kwargs):
    try:
        monitor = instance.monitor
    except:
        monitor, created = Monitor.objects.get_or_create(user=instance)
        monitor.save()
        Group.objects.get_or_create(name='%s_admin' % monitor.country)
