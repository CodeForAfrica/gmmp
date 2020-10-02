from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian import shortcuts
from django.contrib.auth.models import Group

from . import models
from gmmp.models import SpecialQuestions

class PermsAdmin(GuardedModelAdmin):

    def save_model(self, request, obj, form, change):
        """
        Get the country from the user creating the model instance,
        and relate it to the appropriate CountryRegion model.

        """
        country = request.user.monitor.country
        obj.monitor = request.user.monitor
        obj.monitor_code = form.cleaned_data['monitor_code']
        obj.country = country
        obj.country_region = models.CountryRegion.objects.get(country=country)
        obj.save()
        self.assign_permissions(request.user, obj)

    def perms_queryset(self, request, perm):
        if request.user.is_superuser:
            return super(PermsAdmin, self).get_queryset(request)

        return shortcuts.get_objects_for_user(request.user, [perm])

    def get_queryset(self, request):
        qs = self.perms_queryset(request, 'forms.change_%s' % self.permcode)
        return qs.filter(country=request.user.monitor.country) if not request.user.is_superuser else qs

    def assign_permissions(self, user, obj):
        country = user.monitor.country
        shortcuts.assign_perm('forms.change_%s' % self.permcode, user, obj)
        shortcuts.assign_perm('forms.add_%s' % self.permcode, user, obj)
        shortcuts.assign_perm('forms.delete_%s' % self.permcode, user, obj)

        group, _ = Group.objects.get_or_create(name='%s_admin' % country)
        shortcuts.assign_perm('forms.change_%s' % self.permcode, group, obj)
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        response = super(PermsAdmin, self).render_change_form(request, context, add, change, form_url, obj)
        response.context_data['title'] = _("Add Article")
        return response
    
    def delete_model(self, request, obj):
        obj.deleted = True
        # Mark all Newspaper Person and Journalists as deleted too
        obj.newspaperperson_set.update(deleted=True)
        obj.newspaperjournalist_set.update(deleted=True)
        obj.save()
        return

# Inline Elements:

# Journalists & Reporters
# -----------------------

class NewspaperJournalistInline(admin.TabularInline):
    model = models.NewspaperJournalist
    extra = 1
    verbose_name_plural = _('''For each newspaper story, you should code each journalist/reporter who wrote the story and whose name appears.
<br/>
<strong>Do not code:</strong>
<br/>
Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent')
<br/>
News agencies''')
    exclude = ('age', 'deleted', )

class RadioJournalistInline(admin.TabularInline):
    model = models.RadioJournalist
    extra = 1
    verbose_name_plural = _('''Use one line on the coding sheet for:
<br/>
Each news anchor or announcer: <strong>Code the anchor/announcer in each story, even if it is the same person.</strong>
<br/>
Each reporter''')
    exclude = ('age', 'deleted', )

    fieldsets = [
        ('', {
            'fields': ('role', 'sex')
        }),
    ]

class TelevisionJournalistInline(admin.TabularInline):
    model = models.TelevisionJournalist
    extra = 1
    verbose_name_plural = _('''Use one line on the coding sheet for:
<br/>
Each news anchor or announcer: <strong>Code the anchor/announcer in each story, even if it is the same person.</strong>
<br/>
Each reporter''')
    exclude = ('deleted', )

    fieldsets = [
        ('', {
            'fields': ('role', 'sex', 'age')
        }),
    ]

class InternetJournalistInline(admin.TabularInline):
    model = models.InternetNewsJournalist
    extra = 1
    verbose_name_plural = _('''For each online news story, you should code each journalist/reporter who wrote the story and whose name appears.
<br/>
<strong>Do not code:</strong>
<br/>
Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent')
<br/>
News agencies''')
    exclude = ('deleted', )

class TwitterJournalistInline(admin.TabularInline):
    model = models.TwitterJournalist
    extra = 1
    verbose_name_plural = _('''<strong>Click on the link in the tweet leading to the full story to see the name of the journalist or reporter.</strong>
<br />
For each online news story, you should code each journalist/reporter who wrote the story and whose name appears.
<br/>
<strong>Do not code:</strong>
<br/>
Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent')
<br/>
News agencies''')
    exclude = ('deleted', )



# People In The News
# ------------------
class PersonInTheNewsInLine(admin.StackedInline):
    exclude = ('deleted', )
    def get_formset(self, request, obj=None, **kwargs):
            form = super(PersonInTheNewsInLine, self).get_formset(request, obj, **kwargs)
            country = request.user.monitor.country
            country_special_questions = SpecialQuestions.objects.filter(country=country).first()
            if country_special_questions:
                question_1 = country_special_questions.question_1
                if question_1:
                    label_1 = form.form.base_fields['special_qn_1'].label
                    form.form.base_fields['special_qn_1'].label = '{}: {}'.format(label_1, question_1)
                question_2 = country_special_questions.question_2
                if question_2:
                    label_2 = form.form.base_fields['special_qn_2'].label
                    form.form.base_fields['special_qn_2'].label = '{}: {}'.format(label_2, question_2)
                question_3 = country_special_questions.question_3
                if question_3:
                    label_3 = form.form.base_fields['special_qn_3'].label
                    form.form.base_fields['special_qn_3'].label = '{}: {}'.format(label_3, question_3)

            return form

class NewspaperPersonInline(PersonInTheNewsInLine):
    model = models.NewspaperPerson
    radio_fields = {
        'family_role': admin.HORIZONTAL,
        'victim_or_survivor': admin.HORIZONTAL,
        'is_quoted': admin.HORIZONTAL,
    }
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the article')
    verbose_name = _('Person mentioned in the article')

class RadioPersonInline(PersonInTheNewsInLine):
    model = models.RadioPerson
    radio_fields = {
        'family_role': admin.HORIZONTAL,
        'victim_or_survivor': admin.HORIZONTAL,
    }
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the broadcast')
    verbose_name = _('Person mentioned in the broadcast')

class TelevisionPersonInline(PersonInTheNewsInLine):
    model = models.TelevisionPerson
    inline_classes = ('grp-collapse grp-open',)
    radio_fields = {
        'family_role': admin.HORIZONTAL,
        'victim_or_survivor': admin.HORIZONTAL,
    }
    extra = 1
    verbose_name_plural = _('People in the broadcast')
    verbose_name = _('Person mentioned in the broadcast')

class InternetNewsPersonInline(PersonInTheNewsInLine):
    model = models.InternetNewsPerson
    radio_fields = {
        'family_role': admin.HORIZONTAL,
        'victim_or_survivor': admin.HORIZONTAL,
        'is_quoted': admin.HORIZONTAL,
    }
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the news')
    verbose_name = _('Person in the news')

class TwitterPersonInline(PersonInTheNewsInLine):
    model = models.TwitterPerson
    inline_classes = ('grp-collapse grp-open',)
    extra = 1
    verbose_name_plural = _('People in the tweet')
    verbose_name = _('Person mentioned in the tweet')


# Forms
# -----

basic_filters = ('topic', 'about_women', 'stereotypes', 'further_analysis')

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
        (_('Format'), {
            'fields': (
                'monitor_mode',
            ),
        }),
        (_('Basic information'), {
            'fields': (
                'monitor_code',
                'newspaper_name',
            ),
        }),
        (_('Story'), {
            'fields': (
                'page_number', 'covid19', 'topic', 'scope', 'space',
            ),
        }),
        (_('Analysis'), {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        (_('Journalists & Reporters'), {
            'description': _('''Column 9 is for the journalist or reporter. For each story, code each journalist/reporter who wrote the story and whose name appears. Code each journalist/reporter in a separate row.
            <br/>\n
            Do not code: (i) Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent'); (ii) News agencies'''),
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        (_('People in the news'), {
            'description': _('''Columns 10 - 22 are for people in the news.
            <br/>\n
            Code (i) any person whom the story is about, even if they are not interviewed or quoted; (ii) Each person who is interviewed,  (iii) Each person in the story who is quoted, either directly or indirectly.'''),
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        (_('Does this story warrant further analysis?'), {
            'description': _('''A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women’s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women’s human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select ‘1’ (Yes), you will need to send a copy of the clipping to your national/regional coordinator.</small>'''),
            'fields': ('further_analysis',),
        }),
        (_('Comments & Explanations'), {
            'fields' : ('comments',),
        }),
    ]

    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_fields_newspaper.js',
            'forms/admin/dependent_fields.js',
            'forms/admin/check_tab_errors/check.js',
            'forms/admin/check_tab_errors/newspaperperson.js',
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
        (_('Format'), {
            'fields': (
                'monitor_mode',
            ),
        }),
        (_('Basic information'), {
            'fields': (
                'monitor_code',
                'channel', 'start_time',
                'num_female_anchors', 'num_male_anchors',
            ),
        }),
        (_('Story'), {
            'fields': (
                'item_number', 'covid19', 'topic', 'scope',
            ),
        }),
        (_('Analysis'), {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        (_('Journalists & Reporters'), {
            'description': _('''Columns 8 and 9 are for journalists, presenters, anchors, reporters, etc. Code the anchor/announcer even if it is the same person for each news item. Code each reporter and journalist'''),
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        (_('People in the news'), {
            'description': _(''' Columns 10 to 19 are for people in the news. Code: (i) Each person in the story who speaks (ii) any person whom the story is about, even if they do not speak. Code only individual people. Code each person in a separate row.
            Do not code: (i) Groups (e.g. a group of nurses, a group of soldiers); (ii) Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the story is about them); (iv)Deceased historical figures (unless the story is about them); Interpreters (Code the person being interviewed as if they spoke without an interpreter).'''),
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        (_('Does this story warrant further analysis?'), {
            'description': _('''A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women’s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women’s human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select ‘1’ (Yes), you will need to send a copy of the recording to your national/regional coordinator.</small>'''),
            'fields': ('further_analysis',),
        }),
    ]

    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_radio_fields.js',
            'forms/admin/dependent_fields.js',
            'forms/admin/check_tab_errors/check.js',
            'forms/admin/check_tab_errors/radioperson.js',
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
        (_('Format'), {
            'fields': (
                'monitor_mode',
            ),
        }),
        (_('Basic information'), {
            'fields': (
                'monitor_code',
                'channel', 'start_time',
                'num_female_anchors', 'num_male_anchors',
            ),
        }),
        (_('Story'), {
            'fields': (
                'item_number', 'covid19', 'topic', 'scope',
            ),
            'classes' : ('story-fieldset',),
        }),
        (_('Analysis'), {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        (_('Journalists & Reporters'), {
            'description': _('''Columns 8, 9 and 10 are for journalists, presenters, anchors, reporters, etc. Code the anchor/announcer even if it is the same person for each news item. Code each reporter and journalist. Code each person in a separate row'''),
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        (_('People in the news'), {
            'description': _('''Columns 11 to 21 are for people in the news. Code each person in the story who speaks, and any person whom the story is about, even if they do not speak.
            Code only individual people.
            Do not code: (i) Groups (e.g. a group of nurses, a group of soldiers); (ii) Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the story is about them); (iv) Deceased historical figures (unless the story is about them); (v) Interpreters (Code the person being interviewed as if they spoke without an interpreter).'''),
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        (_('Does this story warrant further analysis?'), {
            'description': _('''A story warrants further analysis if it clearly perpetuates or alternatively challenges gender stereotypes, if it includes women’s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women’s human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select ‘1’ (Yes), you will need to send a copy of the recording to your national/regional coordinator.</small>'''),
            'fields': ('further_analysis',),
        }),
        (_('Comments & Explanations'), {
            'fields' : ('comments',),
        }),
    ]

    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_television_fields.js',
            'forms/admin/dependent_fields.js',
            'forms/admin/check_tab_errors/check.js',
            'forms/admin/check_tab_errors/televisionperson.js',
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
        (_('Format'), {
            'fields': (
                'monitor_mode',
            ),
        }),
        (_('Basic information'), {
            'fields': (
                'monitor_code',
                'website_name', 'website_url', 'time_accessed', 'offline_presence'
            ),
        }),
        ('Story', {
            'fields': ('webpage_layer_no', 'covid19', 'topic', 'scope', 'shared_via_twitter', 'shared_on_facebook'),
        }),
        ('Analysis', {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        (_('Journalists & Reporters'), {
            'description': _('''Columns 10 and 11 are for the reporter or journalist. For each story, code each journalist/reporter (i) who wrote the story and whose name appears, or (ii) who is visible in video clips, or (ii) who voice is heard in audio clips. Code each journalist/reporter in a separate row.
            Do not code: (i) Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent'); (ii) News agencies.'''),
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        (_('People in the news'), {
            'description': _('''Columns 12 to 24 are for people in the news whether in the text or in video clips. Code (i) any person whom the story is about even if they are not interviewed or quoted; (ii) Each person who is interviewed, (iii) Each person in the story who is quoted, either directly or indirectly. Code only individual people.
            Do not code: (i) Groups (e.g. a group of nurses, a group of soldiers); (ii) Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the story is about them); (iv) Deceased historical figures (unless the story is about them); (v) Interpreters (Code the person being interviewed as if they spoke without an interpreter).'''),
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        (_('Does this story warrant further analysis?'), {
            'description': _('''A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select '1' (Yes), you will need to send a print-out of the story, screen grab of the page and recordings of multimedia features in it to your national/regional coordinator.</small>'''),
            'fields': ('further_analysis',),
        }),
        (_('Comments & Explanations'), {
            'fields' : ('url_and_multimedia',),
        }),
    ]

    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_internet_fields.js',
            'forms/admin/dependent_fields.js',
            'forms/admin/check_tab_errors/check.js',
            'forms/admin/check_tab_errors/internetnewsperson.js',
        ]

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
        'equality_rights': admin.HORIZONTAL,
        'about_women': admin.HORIZONTAL,
        'inequality_women': admin.HORIZONTAL,
        'stereotypes': admin.HORIZONTAL,
        'further_analysis': admin.HORIZONTAL,
    }

    fieldsets = [
        (_('Format'), {
            'fields': (
                'monitor_mode',
            ),
        }),
        (_('Basic information'), {
            'fields': (
                'monitor_code',
                'media_name', 'twitter_handle'
            ),
        }),
        (_('Tweet'), {
            'fields': (
                'retweet', 'covid19', 'topic'
            ),
            'classes' : ('story-fieldset',),
        }),
        (_('Analysis'), {
            'fields' : ('equality_rights', 'about_women', 'inequality_women', 'stereotypes'),
        }),
        (_('Journalists & Reporters'), {
            'description': _('''Columns 7 and 8 are for the reporter or journalist. Code the journalist to who the twitter account belongs if the account does not belong to the media house.
            Code any journalist referenced in the tweet. Code each journalist/reporter in a separate row.
            Do not code: (i) Unnamed journalists (e.g. 'Staff reporter', 'Our correspondent'); (ii) News agencies.'''),
            'fields': (),
            'classes' : ('journalists-fieldset',),
        }),
        (_('People in the news'), {
            'description': _('''Columns 9 - 16 are for people in the tweet. Code (i) any person whom the tweet is about even if they are not interviewed or quoted; (ii) Each person who is interviewed, (iii) Each person in the tweet who is quoted, either directly or indirectly. Code only individual people.
            Do not code: (i) Journalists referenced in the tweet (journalists are coded in questions 7-8); (ii)Groups (e.g. a group of nurses, a group of soldiers); (ii)
            Organisations, companies, collectivities (e.g. political parties); (iii) Characters in novels or movies (unless the tweet is about them); (iv) Deceased historical figures (unless the tweet is about them); (v) Interpreters (Code the person being interviewed as if they spoke without an interpreter).'''),
            'fields': (),
            'classes' : ('people-fieldset',),
        }),
        (_('Does this tweet warrant further analysis?'), {
            'description': _('''A story warrants further analysis if it clearly perpetuates or alternatively challenges gender stereotypes, if it includes women’s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women’s human rights, etc. Consult the guide for further explanation.
            <br/><br/>
            <small>*If you select ‘1’ (Yes), you will need to send a print-out of the tweet and screen grab of the page to your national/regional coordinator.</small>'''),
            'fields': ('further_analysis',),
        }),
        (_('Comments & Explanations'), {
            'fields' : ('url_and_multimedia', ),
        }),
    ]
    list_filter = basic_filters

    class Media:
        js = [
            'forms/admin/move_fields.js',
            'forms/admin/move_twitter_fields.js',
            'forms/admin/dependent_fields.js'
        ]


admin.site.register(models.NewspaperSheet, NewspaperSheetAdmin)
admin.site.register(models.RadioSheet, RadioSheetAdmin)
admin.site.register(models.TelevisionSheet, TelevisionSheetAdmin)
admin.site.register(models.InternetNewsSheet, InternetNewsSheetAdmin)
admin.site.register(models.TwitterSheet, TwitterSheetAdmin)
