from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
import models

class InternetJournalistInline(admin.TabularInline):
    model = models.InternetNewsJournalist
    extra = 1
    verbose_name_plural = _('''Add a new record for each journalist who: 
(i) wrote the story and whose name appears, or 
(ii) is visible in video clips, or 
(iii) can be heard in audio clips. 

Do not code: (i) Unnamed journalists (e.g. ''Staff reporter'', ''Our correspondent''); (ii) News agencies.''')

class TwitterJournalistInline(admin.TabularInline):
    model = models.TwitterJournalist
    extra = 1
    verbose_name_plural = _('''
        Code the journalist to whom the twitter account belongs if the account does not belong to the media house. Code any
journalist referenced in the tweet. Code each journalist/reporter in a separate row.
Do not code: (i) Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent'); (ii) News agencies
''')

class NewspaperJournalistInline(admin.TabularInline):
    model = models.NewspaperJournalist
    extra = 1
    verbose_name_plural = _('''
    For each newspaper story, you should code each journalist/reporter who wrote the story and whose name appears.
<strong>Do not code:</strong>
Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent')
News agencies
''')

class TelevisionJournalistInline(admin.TabularInline):
    model = models.TelevisionJournalist
    extra = 1
    verbose_name_plural = _('''Add a new record for each journalist who: 
(i) wrote the story and whose name appears, or 
(ii) is visible in video clips, or 
(iii) can be heard in audio clips. 

Do not code: (i) Unnamed journalists (e.g. ''Staff reporter'', ''Our correspondent''); (ii) News agencies.''')

class RadioJournalistInline(admin.TabularInline):
    model = models.RadioJournalist
    extra = 1
    verbose_name_plural = _('''Add a new record for each journalist who: 
(i) wrote the story and whose name appears, or 
(ii) is visible in video clips, or 
(iii) can be heard in audio clips. 

Do not code: (i) Unnamed journalists (e.g. ''Staff reporter'', ''Our correspondent''); (ii) News agencies.''')

class JournalistAdmin(admin.ModelAdmin):
    pass

class InternetNewsPersonInline(admin.StackedInline):
    model = models.InternetNewsPerson
    extra = 1
    verbose_name_plural = _('People in the news')
    verbose_name = _('Person in the news')
    # Setting the unicode to blank in the admin
    model.__unicode__ = lambda x : ""

    fieldsets = [

        ('General', {
            'fields': ('sex', 'age', 'occupation', 'function', 'family_role')
        }),
        ('Victim or Survivor', {
            'fields': ('victim_or_survivor', 'victim_of', 'survivor_of')
        }),
        ('News', {
            'fields': ('is_quoted', 'is_photograph')
        }),
    ]

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_internet_fields.js'
        ]

class TwitterPersonInline(admin.StackedInline):
    model = models.TwitterPerson
    extra = 1
    verbose_name_plural = _('People in the tweet')
    verbose_name = _('Person mentioned in the tweet')

class NewspaperPersonInline(admin.StackedInline):
    model = models.NewspaperPerson
    extra = 1
    verbose_name_plural = _('People in the article')
    verbose_name = _('Person mentioned in the article')

class TelevisionPersonInline(admin.StackedInline):
    model = models.TelevisionPerson
    extra = 1
    verbose_name_plural = _('People in the broadcast')
    verbose_name = _('Person mentioned in the broadcast')

class RadioPersonInline(admin.StackedInline):
    model = models.RadioPerson
    extra = 1
    verbose_name_plural = _('People in the broadcast')
    verbose_name = _('Person mentioned In the broadcast')

class TwitterSheetAdmin(admin.ModelAdmin):
    inlines = [
        TwitterPersonInline,
        TwitterJournalistInline,
    ]

    radio_fields = {
        'retweet' : admin.HORIZONTAL,
        'about_women': admin.HORIZONTAL,
        'stereotypes': admin.HORIZONTAL,
        'further_analysis': admin.HORIZONTAL,
    }

    fieldsets = [

        ('Story', {
            'fields': (
                'monitor', 'media_name', 'twitter_handle', 'retweet', 'topic'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'stereotypes', 'further_analysis', 'url_and_multimedia', ),
        }),
    ]

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_twitter_fields.js'
        ]

class InternetNewsSheetAdmin(admin.ModelAdmin):
    inlines = [
        InternetJournalistInline,
        InternetNewsPersonInline,
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
            'classes' : ('story-fieldset',),
        }),
        ('Source', {
            'fields' : ('person_secondary',),
            'classes' : ('source-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'inequality_women', 'stereotypes', 'further_analysis', 'url_and_multimedia', 'comments'),
        }),
    ]

class NewspaperSheetAdmin(admin.ModelAdmin):
    inlines = [
        NewspaperPersonInline,
        NewspaperJournalistInline,
    ]

    radio_fields = {
        'equality_rights': admin.HORIZONTAL,
        'person_secondary': admin.HORIZONTAL,
        'about_women': admin.HORIZONTAL,
        'inequality_women': admin.HORIZONTAL,
        'stereotypes': admin.HORIZONTAL,
        'further_analysis': admin.HORIZONTAL,
    }

    fieldsets = [
        ('Story', {
            'fields': (
                'monitor', 'newspaper_name', 'page_number',
                'topic', 'scope', 'space', 'equality_rights'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Source', {
            'fields' : ('person_secondary',),
            'classes' : ('source-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'inequality_women', 'stereotypes', 'further_analysis', 'comments'),
        }),
    ]

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_fields_newspaper.js'
        ]


class TelevisionSheetAdmin(admin.ModelAdmin):
    inlines = [
        TelevisionPersonInline,
        TelevisionJournalistInline
    ]

    radio_fields = {
        'equality_rights': admin.HORIZONTAL,
        'about_women': admin.HORIZONTAL,
        'inequality_women': admin.HORIZONTAL,
        'stereotypes': admin.HORIZONTAL,
        'further_analysis': admin.HORIZONTAL,
    }

    fieldsets = [
        ('Basic Information', {
            'fields': (
                'monitor', 'station_name', 'television_channel', 'start_time',
                'num_female_anchors', 'num_male_anchors'
            ),
        }),
        ('Story', {
            'fields': (
                'item_number', 'topic', 'scope', 'equality_rights'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'inequality_women', 'stereotypes', 'further_analysis'),
        }),
    ]

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_television_fields.js'
        ]

class RadioSheetAdmin(admin.ModelAdmin):
    inlines = [
        RadioPersonInline,
        RadioJournalistInline,
    ]

    radio_fields = {
        'equality_rights': admin.HORIZONTAL,
        'about_women': admin.HORIZONTAL,
        'inequality_women': admin.HORIZONTAL,
        'stereotypes': admin.HORIZONTAL,
        'further_analysis': admin.HORIZONTAL,
    }

    fieldsets = [
        ('Basic Information', {
            'fields': (
                'monitor', 'station_name', 'start_time',
                'num_female_anchors', 'num_male_anchors'
            ),
        }),
        ('Story', {
            'fields': (
                'item_number', 'topic', 'scope', 'equality_rights'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'inequality_women', 'stereotypes', 'further_analysis'),
        }),
    ]

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_radio_fields.js'
        ]

admin.site.register(models.InternetNewsSheet, InternetNewsSheetAdmin)
admin.site.register(models.TwitterSheet, TwitterSheetAdmin)
admin.site.register(models.NewspaperSheet, NewspaperSheetAdmin)
admin.site.register(models.TelevisionSheet, TelevisionSheetAdmin)
admin.site.register(models.RadioSheet, RadioSheetAdmin)

