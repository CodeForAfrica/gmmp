from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian import shortcuts
from django.contrib.auth.models import Group

import models

class PermsAdmin(GuardedModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.monitor = request.user
        obj.save()
        self.assign_permissions(request.user, obj)

    def perms_queryset(self, request, perm):
        if request.user.is_superuser:
            return super(PermsAdmin, self).get_queryset(request)

        return shortcuts.get_objects_for_user(request.user, [perm])

    def get_queryset(self, request):
        return self.perms_queryset(request, 'forms.change_%s' % self.permcode)

    def assign_permissions(self, user, obj):
        country = user.monitor.country
        shortcuts.assign_perm('forms.change_%s' % self.permcode, user, obj)
        shortcuts.assign_perm('forms.add_%s' % self.permcode, user, obj)
        shortcuts.assign_perm('forms.delete_%s' % self.permcode, user, obj)

        group, _ = Group.objects.get_or_create(name='%s_admin' % country)
        shortcuts.assign_perm('forms.change_%s' % self.permcode, group, obj)

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
    exclude = ('age',)

class NewspaperJournalistInline(admin.TabularInline):
    model = models.NewspaperJournalist
    extra = 1
    verbose_name_plural = _('''
    For each newspaper story, you should code each journalist/reporter who wrote the story and whose name appears.
<strong>Do not code:</strong>
Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent')
News agencies
''')
    exclude = ('age',)                

class TelevisionJournalistInline(admin.TabularInline):
    model = models.TelevisionJournalist
    extra = 1
    verbose_name_plural = _('''Add a new record for each journalist who: 
(i) wrote the story and whose name appears, or 
(ii) is visible in video clips, or 
(iii) can be heard in audio clips. 

Do not code: (i) Unnamed journalists (e.g. ''Staff reporter'', ''Our correspondent''); (ii) News agencies.''')

    fieldsets = [
        ('', {
            'fields': ('role', 'sex', 'age')
        }),
    ]

class RadioJournalistInline(admin.TabularInline):
    model = models.RadioJournalist
    extra = 1
    verbose_name_plural = _('''Add a new record for each journalist who: 
(i) wrote the story and whose name appears, or 
(ii) is visible in video clips, or 
(iii) can be heard in audio clips. 

Do not code: (i) Unnamed journalists (e.g. ''Staff reporter'', ''Our correspondent''); (ii) News agencies.''')
    exclude = ('age',)

    fieldsets = [
        ('', {
            'fields': ('role', 'sex')
        }),
    ]

class JournalistAdmin(admin.ModelAdmin):
    pass

class InternetNewsPersonInline(admin.StackedInline):
    model = models.InternetNewsPerson
    inline_classes = ('grp-collapse grp-open',)
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
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the tweet')
    verbose_name = _('Person mentioned in the tweet')

class NewspaperPersonInline(admin.StackedInline):
    model = models.NewspaperPerson
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the article')
    verbose_name = _('Person mentioned in the article')

class TelevisionPersonInline(admin.StackedInline):
    model = models.TelevisionPerson
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the broadcast')
    verbose_name = _('Person mentioned in the broadcast')

class RadioPersonInline(admin.StackedInline):
    model = models.RadioPerson
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the broadcast')
    verbose_name = _('Person mentioned In the broadcast')

basic_filters = ('topic', 'about_women', 'stereotypes', 'further_analysis')

class TwitterSheetAdmin(PermsAdmin):

    @property
    def permcode(self):
        return 'twittersheet'

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

        ('Basic Information', {
            'fields': (
                'media_name', 'twitter_handle'
            ),
        }),
        ('Story', {
            'fields': (
                'retweet', 'topic'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Comments & Explanations', {
            'fields' : ('url_and_multimedia', ),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'stereotypes', 'further_analysis'),
        }),
    ]
    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_twitter_fields.js'
        ]

class InternetNewsSheetAdmin(PermsAdmin):

    @property
    def permcode(self):
        return 'internetnewssheet'

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
        ('Basic Information', {
            'fields': (
                'website_name', 'website_url', 'time_accessed', 'offline_presence'
            ),
        }),
        ('Story', {
            'fields': (
                'webpage_layer_no', 'topic', 'topic_comments', 'scope', 'shared_via_twitter',
                'shared_on_facebook', 'equality_rights'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Source', {
            'fields' : ('person_secondary',),
            'classes' : ('source-fieldset',),
        }),
        ('Comments & Explanations', {
            'fields' : ('url_and_multimedia',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'inequality_women', 'stereotypes', 'further_analysis'),
        }),
    ]

    list_filter = basic_filters

class NewspaperSheetAdmin(PermsAdmin):

    @property
    def permcode(self):
        return 'newspapersheet'

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
        ('Basic Information', {
            'fields': (
                'newspaper_name',
            ),
        }),
        ('Story', {
            'fields': (
                'page_number', 'topic', 'scope', 'space', 'equality_rights'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Source', {
            'fields' : ('person_secondary',),
            'classes' : ('source-fieldset',),
        }),
        ('Comments & Explanations', {
            'fields' : ('comments',),
        }),
        ('Analysis', {
            'fields' : ('about_women', 'inequality_women', 'stereotypes', 'further_analysis'),
        }),
    ]

    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_fields_newspaper.js'
        ]


class TelevisionSheetAdmin(PermsAdmin):

    @property
    def permcode(self):
        return 'televisionsheet'

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
                'station_name', 'television_channel', 'start_time',
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
        ('Comments & Explanations', {
            'fields' : ('comments',),
        }),
    ]

    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_television_fields.js'
        ]

class RadioSheetAdmin(PermsAdmin):

    @property
    def permcode(self):
        return 'radiosheet'

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
                'station_name', 'start_time',
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
        ('Comments & Explanations', {
            'fields' : ('comments',),
        }),
    ]

    list_filter = basic_filters

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

