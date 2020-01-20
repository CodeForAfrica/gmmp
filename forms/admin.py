from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian import shortcuts
from django.contrib.auth.models import Group

from . import models

class PermsAdmin(GuardedModelAdmin):

    def save_model(self, request, obj, form, change):
        """
        Get the country from the user creating the model instance,
        and relate it to the appropriate CountryRegion model.

        """
        country = request.user.monitor.country
        obj.monitor = request.user.monitor
        obj.country = country
        obj.country_region = models.CountryRegion.objects.get(country=country)
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
        ('Tweet', {
            'fields': (
                'retweet', 'topic'
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        ('Journalists & Reporters', {
            'description': '''Columns 7 and 8 are for the reporter or journalist. Code the journalist to who the twitter account belongs if the account does not belong to the media house.
            Code any journalist referenced in the tweet. Code each journalist/reporter in a separate row.
            Do not code: (i) Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent'); (ii) News agencies.''',
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        ('People In The News', {
            'description': u'''Columns 9 - 16 are for people in the tweet. Code (i) any person whom the tweet is about even if they are not interviewed or quoted; (ii) Each person who is interviewed, (iii) Each person in the tweet who is quoted, either directly or indirectly. Code only individual people.
            Do not code: (i) Journalists referenced in the tweet (journalists are coded in questions 7-8); (ii)Groups (e.g. a group of nurses, a group of soldiers); (ii)
            Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the tweet is about them); (iv) Deceased historical figures (unless the tweet is about them); (v) Interpreters (Code the person being interviewed as if they spoke without an interpreter).''',
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        ('Comments & Explanations', {
            'fields' : ('url_and_multimedia', ),
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
            'fields': ('webpage_layer_no','topic','scope', 'shared_via_twitter', 'shared_on_facebook'),
        }),
        ('Analysis', {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        ('Journalists & Reporters', {
            'description': '''Columns 10 and 11 are for the reporter or journalist. For each story, code each journalist/reporter (i) who wrote the story and whose name appears, or (ii) who is visible in video clips, or (ii) who voice is heard in audio clips. Code each journalist/reporter in a separate row.
            Do not code: (i) Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent'); (ii) News agencies.''',
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        ('People In The News', {
            'description': '''Columns 12 to 24 are for people in the news whether in the text or in video clips. Code (i) any person whom the story is about even if they are not interviewed or quoted; (ii) Each person who is interviewed, (iii) Each person in the story who is quoted, either directly or indirectly. Code only individual people.
            Do not code: (i) Groups (e.g. a group of nurses, a group of soldiers); (ii) Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the story is about them); (iv) Deceased historical figures (unless the story is about them); (v) Interpreters (Code the person being interviewed as if they spoke without an interpreter).''',
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        ('Does this story warrant further analysis?', {
            'description': '''A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select '1' (Yes), you will need to send a print-out of the story, screen grab of the page and recordings of multimedia features in it to your national/regional coordinator.</small>''',
            'fields': ('further_analysis',),
        }),
        ('Comments & Explanations', {
            'fields' : ('url_and_multimedia',),
        }),
    ]

    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_internet_fields.js'
        ]


class NewspaperSheetAdmin(PermsAdmin):

    @property
    def permcode(self):
        return 'newspapersheet'

    inlines = [
        NewspaperJournalistInline,
        NewspaperPersonInline,
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
                'newspaper_name',
            ),
        }),
        ('Story', {
            'fields': (
                'page_number', 'topic', 'scope', 'space',
            ),
        }),
        ('Analysis', {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        ('Journalists & Reporters', {
            'description': '''Column 9 is for the journalist or reporter. For each story, code each journalist/reporter who wrote the story and whose name appears. Code each journalist/reporter in a separate row.
            Do not code: (i) Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent'); (ii) News agencies''',
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        ('People In The News', {
            'description': '''Columns 10 - 22 are for people in the news.
            Code (i) any person whom the story is about, even if they are not interviewed or quoted; (ii) Each person who is interviewed,  (iii) Each person in the story who is quoted, either directly or indirectly.''',
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        ('Does this story warrant further analysis?', {
            'description': '''*A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women’s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women’s human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select ‘1’ (Yes), you will need to send a copy of the clipping to your national/regional coordinator.</small>''',
            'fields': ('further_analysis',),
        }),
        ('Comments & Explanations', {
            'fields' : ('comments',),
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
                'item_number', 'topic', 'scope',
            ),
            'classes' : ('story-fieldset',),
        }),
        ('Analysis', {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        ('Journalists & Reporters', {
            'description': '''Columns 8, 9 and 10 are for journalists, presenters, anchors, reporters, etc. Code the anchor/announcer even if it is the same person for each news item. Code each reporter and journalist. Code each person in a separate row''',
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        ('People In The News', {
            'description': '''Columns 11 to 21 are for people in the news. Code each person in the story who speaks, and any person whom the story is about, even if they do not speak.
            Code only individual people.
            Do not code: (i) Groups (e.g. a group of nurses, a group of soldiers); (ii) Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the story is about them); (iv) Deceased historical figures (unless the story is about them); (v) Interpreters (Code the person being interviewed as if they spoke without an interpreter).''',
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        ('Does this story warrant further analysis?', {
            'description': '''A story warrants further analysis if it clearly perpetuates or alternatively challenges gender stereotypes, if it includes women’s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women’s human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select ‘1’ (Yes), you will need to send a copy of the recording to your national/regional coordinator.</small>''',
            'fields': ('further_analysis',),
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
                'item_number', 'topic', 'scope',
            ),
        }),
        ('Analysis', {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        ('Journalists & Reporters', {
            'description': '''Columns 8 and 9 are for journalists, presenters, anchors, reporters, etc. Code the anchor/announcer even if it is the same person for each news item. Code each reporter and journalist''',
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        ('People In The News', {
            'description': ''' Columns 10 to 19 are for people in the news. Code: (i) Each person in the story who speaks (ii) any person whom the story is about, even if they do not speak. Code only individual people. Code each person in a separate row.
            Do not code: (i) Groups (e.g. a group of nurses, a group of soldiers); (ii) Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the story is about them); (iv)Deceased historical figures (unless the story is about them); Interpreters (Code the person being interviewed as if they spoke without an interpreter).''',
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        ('Does this story warrant further analysis?', {
            'description': '''A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women’s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women’s human rights, etc. Consult the guide for further explanation.
            <br/></br/>
            <small>*If you select ‘1’ (Yes), you will need to send a copy of the recording to your national/regional coordinator.</small>''',
            'fields': ('further_analysis',),
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

