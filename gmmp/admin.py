from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from . import models

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MonitorInline(admin.TabularInline):
    model = models.Monitor
    can_delete = False
    verbose_name_plural = _('Monitor Details')


class SpecialQuestionsInline(admin.StackedInline):
    model = models.SpecialQuestions
    can_delete = False
    verbose_name_plural = _('Special Questions')

def monitor_country(obj):
    return obj.monitor.country.name
monitor_country.short_description = _('Country')
monitor_country.admin_order_field = 'monitor__country'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (MonitorInline, SpecialQuestionsInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', monitor_country)
    list_filter = ('monitor__country',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'monitor__country')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
