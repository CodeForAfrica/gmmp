from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

import models

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MonitorInline(admin.TabularInline):
    model = models.Monitor
    can_delete = False
    verbose_name_plural = 'Monitor Details'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (MonitorInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
