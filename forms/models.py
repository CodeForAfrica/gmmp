from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelutils import *

class InternetNewsJournalist(Journalist):
    internetnews_sheet = models.ForeignKey('InternetNewsSheet')

class InternetNewsPerson(Person):
    sex = field_sex
    age = field_age
    occupation = field_occupation
    function = field_function
    family_role = field_family_role
    victim_or_survivor = field_victim_or_survivor
    victim_of = field_victim_of
    survivor_of = field_survivor_of
    is_quoted = field_is_quoted
    is_photograph = field_is_photograph

    internetnews_sheet = models.ForeignKey('InternetNewsSheet')

class InternetNewsSheet(SheetModel):
    # Story
    website_name = models.CharField(max_length=255, verbose_name=_('Website Name'))
    website_url = models.CharField(max_length=255, verbose_name=_('URL'))
    time_accessed = models.DateTimeField(verbose_name=_('Date and Time Accessed'))
    offline_presence = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Offline presence?'))
    
    webpage_layer_no = models.PositiveIntegerField(choices=NUMBER_OPTIONS, help_text=_('Webpage Layer Number. Homepage=1, One click away=2, Five clicks away= 5, etc. Note that if a story appears on the front page, code with 1'), verbose_name=_('Webpage Layer Number'))
    topic = field_topic
    topic_comments = models.TextField(verbose_name=_('Topic Comments'), help_text=_('Complete if no topic above is applicable'), blank=True)
    scope = field_scope
    shared_via_twitter = models.CharField(max_length=1, choices=YESNO, help_text=_('''Has this story been shared by the media house via Twitter?

<br>Enter the exact URL of the story into <a href="http://topsy.com/" target="_blank">http://topsy.com</a> - answer yes if the media house's name appears in the search results.'''), verbose_name=_('Shared via Twitter'))
    shared_on_facebook = models.CharField(max_length=1, choices=YESNO, help_text=_('Has this story been shared by the media house on its Facebook Page?'), verbose_name=_('Shared on Facebook'))
    equality_rights = field_equality_rights

    person_secondary = field_person_secondary
    # Analysis
    about_women = field_about_women(_('story'))
    inequality_women = field_inequality_women(_('story'))
    stereotypes = field_stereotypes('story')
    further_analysis = field_further_analysis(_('story'))
    url_and_multimedia = field_url_and_multimedia('story')

    def __unicode__(self):
        return self.website_url

    class Meta:
        verbose_name = _('Internet News Submission')


class TwitterJournalist(Journalist):
    twitter_sheet = models.ForeignKey('TwitterSheet')

class TwitterPerson(Person):
    sex = field_sex
    is_photograph = field_is_photograph

    twitter_sheet = models.ForeignKey('TwitterSheet')

class TwitterSheet(SheetModel):
    class Meta:
        verbose_name = _('Twitter Submission')

    media_name = models.CharField(max_length=255, verbose_name=_('Media Name'), help_text=_('''For example. 'CNN Breaking News' '''))
    twitter_handle = models.CharField(max_length=255, verbose_name=_('Twitter Handle'), help_text=_('e.g. https://twitter.com/cnnbrk'))

    # Story
    retweet = models.PositiveIntegerField(choices=RETWEET, 
        verbose_name=_('Tweet or Retweet'),
        help_text=_('Only retweets from the same media house can be coded. Do not code retweets from other news providers')
    )
    topic = field_topic
    comments = field_comments
    url_and_multimedia = field_url_and_multimedia('tweet')

    # Analysis
    about_women = field_about_women(_('tweet'))
    stereotypes = field_stereotypes(_('tweet'))
    further_analysis = field_further_analysis(_('tweet'))

class NewspaperJournalist(Journalist):
    newspaper_sheet = models.ForeignKey('NewspaperSheet')

class NewspaperPerson(Person):
    sex = field_sex
    age = field_age
    occupation = field_occupation
    function = field_function
    family_role = field_family_role
    victim_or_survivor = field_victim_or_survivor
    victim_of = field_victim_of
    survivor_of = field_survivor_of
    is_quoted = field_is_quoted
    is_photograph = field_is_photograph

    newspaper_sheet = models.ForeignKey('NewspaperSheet')

class NewspaperSheet(SheetModel):
    class Meta:
        verbose_name = _('Newspaper Submission')

    newspaper_name = models.CharField(max_length=255, verbose_name=_('Newspaper'), help_text=_('''Be as specific as possible. If the paper has different regional editions, write in the name of the edition you are monitoring - e.g. 'The Hindu - Delhi edition'.'''))
    page_number = models.PositiveIntegerField(choices=NUMBER_OPTIONS, verbose_name=_('Page Number'), help_text=_('Write in the number of the page on which the story begins. Story appears on first page = 1, Seventh page = 7, etc.'))
    topic = field_topic
    scope = field_scope
    space = models.PositiveIntegerField(choices=SPACE, verbose_name=_('Space'))
    equality_rights = field_equality_rights
    person_secondary = field_person_secondary
    comments = field_comments
    about_women = field_about_women(_('story'))
    inequality_women = field_inequality_women(_('story'))
    stereotypes = field_stereotypes(_('story'))
    further_analysis = field_further_analysis('story')

class TelevisionPerson(Person):
    sex = field_sex
    age = field_age
    occupation = field_occupation
    function = field_function
    family_role = field_family_role
    victim_or_survivor = field_victim_or_survivor
    victim_of = field_victim_of
    survivor_of = field_survivor_of

    television_sheet = models.ForeignKey('TelevisionSheet')

class TelevisionJournalist(BroadcastJournalist):
    television_sheet = models.ForeignKey('TelevisionSheet')

class TelevisionSheet(SheetModel):
    station_name = models.CharField(max_length=255, verbose_name=_('Name of TV Station'), help_text=_('''Name of the television channel or station : Be as specific as possible. E.g. if the television company is called RTV, and if the newscast is broadcast on its second channel, write in 'RTV-2' '''))

    television_channel = models.CharField(max_length=255, verbose_name=_('Channel'), help_text=_('''Be as specific as possible. E.g. if the television company is called RTV, and if the newscast is broadcast on its second channel, write in 'RTV-2' '''))
    start_time = models.TimeField(verbose_name=_('Time of Broadcast'))
    num_female_anchors = field_num_female_anchors
    num_male_anchors = field_num_male_anchors
    item_number = field_item_number
    topic = field_topic
    scope = field_scope
    equality_rights = field_equality_rights
    about_women = field_about_women(_('story'))
    inequality_women = field_inequality_women(_('story'))
    stereotypes = field_stereotypes(_('story'))
    further_analysis = field_further_analysis('story')
    comments = field_comments

    class Meta:
        verbose_name = _('Television Submission')


class RadioPerson(Person):
    sex = field_sex
    occupation = field_occupation
    function = field_function
    family_role = field_family_role
    victim_or_survivor = field_victim_or_survivor
    victim_of = field_victim_of
    survivor_of = field_survivor_of

    radio_sheet = models.ForeignKey('RadioSheet')

class RadioJournalist(BroadcastJournalist):
    radio_sheet = models.ForeignKey('RadioSheet')

class RadioSheet(SheetModel):
    station_name = models.CharField(max_length=255, verbose_name=_('Name of radio channel or station'), help_text=_('''Be as specific as possible. E.g. if the radio company is called RRI, and if the newscast is broadcast on its third channel, write in 'RRI-3'.'''))

    start_time = models.TimeField(verbose_name=_('Time of Broadcast'))
    num_female_anchors = field_num_female_anchors
    num_male_anchors = field_num_male_anchors
    item_number = field_item_number
    topic = field_topic
    scope = field_scope
    equality_rights = field_equality_rights
    about_women = field_about_women(_('story'))
    inequality_women = field_inequality_women(_('story'))
    stereotypes = field_stereotypes(_('story'))
    further_analysis = field_further_analysis('story')
    comments = field_comments

    class Meta:
        verbose_name = _('Radio Submission')
