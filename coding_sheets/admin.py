from django.contrib import admin

from coding_sheets.models import ProcessedSheet, UnProccessedRow

# Register your models here.

admin.site.register(ProcessedSheet)
admin.site.register(UnProccessedRow)
