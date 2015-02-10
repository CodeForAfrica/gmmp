from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
import models

class JournalistInline(admin.TabularInline):
    model = models.Journalist
    verbose_name_plural = _('''Add a new record for each journalist who: 
(i) wrote the story and whose name appears, or 
(ii) is visible in video clips, or 
(iii) can be heard in audio clips. 

Do not code: (i) Unnamed journalists (e.g. ''Staff reporter'', ''Our correspondent''); (ii) News agencies.''')

class PersonInline(admin.StackedInline):
    model = models.Person
    verbose_name_plural = _('People in the news')

    class Media:
        js = ['forms/admin/move_fields.js']

class InternetNewsSheetAdmin(admin.ModelAdmin):
    inlines = [
        JournalistInline,
        PersonInline,
    ]

    radio_fields = {
        'shared_via_twitter': admin.HORIZONTAL,
        'shared_on_facebook': admin.HORIZONTAL,
        'equality_rights': admin.HORIZONTAL,
        'person_secondary': admin.HORIZONTAL,
        'about_women': admin.HORIZONTAL,
        'inequality_women': admin.HORIZONTAL,
        'stereotypes': admin.HORIZONTAL,
        'further_analysis': admin.HORIZONTAL,
        'offline_presence': admin.HORIZONTAL,
    }

    fieldsets = [
        ('Story', {
            'fields': (
                'monitor', 'website_name', 'website_url', 'time_accessed', 'offline_presence', 'webpage_layer_no',
                'topic', 'topic_comments', 'scope', 'shared_via_twitter', 'shared_on_facebook', 'equality_rights'
            ),
        }),
        ('Source', {
            'fields' : ('person_secondary',),
            'classes' : ('source-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'inequality_women', 'stereotypes', 'further_analysis', 'url_and_multimedia', 'comments'),
        }),
    ]

admin.site.register(models.InternetNewsSheet, InternetNewsSheetAdmin)

