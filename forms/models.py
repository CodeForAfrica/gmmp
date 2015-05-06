from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelutils import *

def prepend_verbose(mydict, field_name, num):
    field = mydict[field_name]
    field.verbose_name = '(%s) %s' % (num, field_name)

class InternetNewsJournalist(Journalist):
    internetnews_sheet = models.ForeignKey('InternetNewsSheet')

class InternetNewsPerson(Person):

    sex = field_sex('10')
    age = field_age('11')
    occupation = field_occupation('12')
    function = field_function('13')
    family_role = field_family_role('14')
    victim_or_survivor = field_victim_or_survivor('15')
    victim_of = field_victim_of('16')
    survivor_of = field_survivor_of('17')
    is_quoted = field_is_quoted('18')
    is_photograph = field_is_photograph('19')

    internetnews_sheet = models.ForeignKey('InternetNewsSheet')

class InternetNewsSheet(SheetModel):

    def __init__(self, *args, **kwargs):
        super(InternetNewsSheet, self).__init__(*args, **kwargs)
    # Story
    website_name = models.CharField(max_length=255, verbose_name=_('Website Name'))
    website_url = models.CharField(max_length=255, verbose_name=_('URL'))
    time_accessed = models.DateTimeField(verbose_name=_('Date and Time Accessed'))
    offline_presence = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Offline presence?'))

    webpage_layer_no = models.PositiveIntegerField(help_text=_('Webpage Layer Number. Homepage=1, One click away=2, Five clicks away= 5, etc. Note that if a story appears on the front page, code with 1'), verbose_name=_('(1) Webpage Layer Number'))
    topic = field_topic('2')
    topic_comments = models.TextField(verbose_name=_('(2a) Topic Comments'), help_text=_('Complete if no topic above is applicable'), blank=True)
    scope = field_scope('3')
    shared_via_twitter = models.CharField(max_length=1, verbose_name=_('(4) Shared via twitter?'), choices=YESNO, help_text=_('''Has this story been shared by the media house via Twitter?

<br>Enter the exact URL of the story into <a href="http://topsy.com/" target="_blank">http://topsy.com</a> - answer yes if the media house's name appears in the search results.'''))
    shared_on_facebook = models.CharField(max_length=1, choices=YESNO, verbose_name=_('(5) Shared on Facebook'), help_text=_('Has this story been shared by the media house on its Facebook Page?'))
    equality_rights = field_equality_rights(6)

    person_secondary = field_person_secondary(9)
    # Analysis
    about_women = field_about_women('21', _('story'))
    inequality_women = field_inequality_women('22', _('story'))
    stereotypes = field_stereotypes('23', 'story')
    further_analysis = field_further_analysis('24', _('story'))
    url_and_multimedia = field_url_and_multimedia('20', 'story')

    def __unicode__(self):
        return self.website_url

    class Meta:
        verbose_name = _('Internet News Submission')

def twitter_journalist_meta(name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[0][0],
        'age' : bases[0]._meta.get_fields_with_model()[1][0],
    }
    prepend_verbose(dct, 'sex', '3')
    return type(name, bases, mydict)

class TwitterJournalist(Journalist):
    __metaclass__ = twitter_journalist_meta

    twitter_sheet = models.ForeignKey('TwitterSheet')

class TwitterPerson(Person):
    sex = field_sex('4')
    is_photograph = field_is_photograph('5')

    twitter_sheet = models.ForeignKey('TwitterSheet')

class TwitterSheet(SheetModel):
    class Meta:
        verbose_name = _('Twitter Submission')

    media_name = models.CharField(max_length=255, verbose_name=_('Media Name'), help_text=_('''For example. 'CNN Breaking News' '''))
    twitter_handle = models.CharField(max_length=255, verbose_name=_('Twitter Handle'), help_text=_('e.g. https://twitter.com/cnnbrk'))

    # Story
    retweet = models.PositiveIntegerField(choices=RETWEET,
        verbose_name=_('(1) Tweet or Retweet'),
        help_text=_('Only retweets from the same media house can be coded. Do not code retweets from other news providers')
    )
    topic = field_topic('2')
    comments = field_comments('TODO should this be here?')
    url_and_multimedia = field_url_and_multimedia('6', 'tweet')

    # Analysis
    about_women = field_about_women('7', _('tweet'))
    stereotypes = field_stereotypes('8', _('tweet'))
    further_analysis = field_further_analysis('9', _('tweet'))

    def __unicode__(self):
        return self.twitter_handle

def newspaper_journalist_meta (name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[0][0],
        'age' : bases[0]._meta.get_fields_with_model()[1][0],
    }
    prepend_verbose(dct, 'sex', '6')
    return type(name, bases, mydict)

class NewspaperJournalist(Journalist):
    __metaclass__ = newspaper_journalist_meta

    newspaper_sheet = models.ForeignKey('NewspaperSheet')

class NewspaperPerson(Person):
    sex = field_sex('8')
    age = field_age('9')
    occupation = field_occupation('10')
    function = field_function('11')
    family_role = field_family_role('12')
    victim_or_survivor = field_victim_or_survivor('13')
    victim_of = field_victim_of('14')
    survivor_of = field_survivor_of('15')
    is_quoted = field_is_quoted('16')
    is_photograph = field_is_photograph('17')

    newspaper_sheet = models.ForeignKey('NewspaperSheet')

class NewspaperSheet(SheetModel):
    class Meta:
        verbose_name = _('Newspaper Submission')

    newspaper_name = models.CharField(max_length=255, verbose_name=_('Newspaper'), help_text=_('''Be as specific as possible. If the paper has different regional editions, write in the name of the edition you are monitoring - e.g. 'The Hindu - Delhi edition'.'''))
    page_number = models.PositiveIntegerField(verbose_name=_('(1) Page Number'), help_text=_('Write in the number of the page on which the story begins. Story appears on first page = 1, Seventh page = 7, etc.'))
    topic = field_topic('2')
    scope = field_scope('3')
    space = models.PositiveIntegerField(choices=SPACE, verbose_name=_('(4) Space'))
    equality_rights = field_equality_rights('5')
    person_secondary = field_person_secondary('7')
    comments = field_comments('18')
    about_women = field_about_women('19', _('story'))
    inequality_women = field_inequality_women('20', _('story'))
    stereotypes = field_stereotypes('21', _('story'))
    further_analysis = field_further_analysis('22', 'story')

    def __unicode__(self):
        return self.newspaper_name

class TelevisionPerson(Person):
    sex = field_sex('8')
    age = field_age('9')
    occupation = field_occupation('10')
    function = field_function('11')
    family_role = field_family_role('12')
    victim_or_survivor = field_victim_or_survivor('13')
    victim_of = field_victim_of('14')
    survivor_of = field_survivor_of('15')

    television_sheet = models.ForeignKey('TelevisionSheet')

def television_journalist_meta(name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[0][0],
        'age' : bases[0]._meta.get_fields_with_model()[1][0],
        'role' : bases[0]._meta.get_fields_with_model()[2][0],
    }

    prepend_verbose(dct, 'role', '5')
    prepend_verbose(dct, 'sex', '6')
    prepend_verbose(dct, 'age', '7')
    return type(name, bases, mydict)

class TelevisionJournalist(BroadcastJournalist):
    __metaclass__ = television_journalist_meta

    television_sheet = models.ForeignKey('TelevisionSheet')

class TelevisionSheet(SheetModel):
    station_name = models.CharField(max_length=255, verbose_name=_('Name of TV Station'), help_text=_('''Name of the television channel or station : Be as specific as possible. E.g. if the television company is called RTV, and if the newscast is broadcast on its second channel, write in 'RTV-2' '''))

    television_channel = models.CharField(max_length=255, verbose_name=_('Channel'), help_text=_('''Be as specific as possible. E.g. if the television company is called RTV, and if the newscast is broadcast on its second channel, write in 'RTV-2' '''))
    start_time = models.TimeField(verbose_name=_('Time of Broadcast'))
    num_female_anchors = field_num_female_anchors
    num_male_anchors = field_num_male_anchors
    item_number = field_item_number('1')
    topic = field_topic('2')
    scope = field_scope('3')
    equality_rights = field_equality_rights('4')
    about_women = field_about_women('16', _('story'))
    inequality_women = field_inequality_women('17', _('story'))
    stereotypes = field_stereotypes('18', _('story'))
    further_analysis = field_further_analysis('19', 'story')
    comments = field_comments('N/A')

    def __unicode__(self):
        return self.station_name

    class Meta:
        verbose_name = _('Television Submission')

class RadioPerson(Person):
    sex = field_sex('7')
    occupation = field_occupation('8')
    function = field_function('9')
    family_role = field_family_role('10')
    victim_or_survivor = field_victim_or_survivor('11')
    victim_of = field_victim_of('12')
    survivor_of = field_survivor_of('13')

    radio_sheet = models.ForeignKey('RadioSheet')

def radio_journalist_meta(name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[1][0],
        'role' : bases[0]._meta.get_fields_with_model()[2][0],
    }
    prepend_verbose(dct, 'role', '5')
    prepend_verbose(dct, 'sex', '6')
    return type(name, bases, mydict)

class RadioJournalist(BroadcastJournalist):
    __metaclass__ = radio_journalist_meta

    radio_sheet = models.ForeignKey('RadioSheet')

class RadioSheet(SheetModel):
    station_name = models.CharField(max_length=255, verbose_name=_('Name of radio channel or station'), help_text=_('''Be as specific as possible. E.g. if the radio company is called RRI, and if the newscast is broadcast on its third channel, write in 'RRI-3'.'''))

    start_time = models.TimeField(verbose_name=_('Time of Broadcast'))
    num_female_anchors = field_num_female_anchors
    num_male_anchors = field_num_male_anchors
    item_number = field_item_number('1')
    topic = field_topic('2')
    scope = field_scope('3')
    equality_rights = field_equality_rights('4')
    about_women = field_about_women('14', _('story'))
    inequality_women = field_inequality_women('15', _('story'))
    stereotypes = field_stereotypes('16', _('story'))
    further_analysis = field_further_analysis('17', 'story')
    comments = field_comments('N/A')

    def __unicode__(self):
        return self.station_name

    class Meta:
        verbose_name = _('Radio Submission')
