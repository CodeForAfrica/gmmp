from collections import OrderedDict

from django.db import models
from django.utils.translation import ugettext_lazy as _
from .modelutils import *

def prepend_verbose(mydict, field_name, num):
    field = mydict[field_name]
    field.verbose_name = '(%s) %s' % (num, field_name)


# ----------------------------
# Newspaper
# ----------------------------

def newspaper_journalist_meta (name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[0][0],
        'age' : bases[0]._meta.get_fields_with_model()[1][0],
    }
    prepend_verbose(dct, 'sex', '9')
    return type(name, bases, mydict)

class NewspaperJournalist(Journalist):
    __metaclass__ = newspaper_journalist_meta

    newspaper_sheet = models.ForeignKey('NewspaperSheet', on_delete=models.CASCADE)

class NewspaperPerson(Person):
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

    special_qn_1 = field_special_qn('20', '1')
    special_qn_2 = field_special_qn('21', '2')
    special_qn_3 = field_special_qn('22', '3')

    newspaper_sheet = models.ForeignKey('NewspaperSheet', on_delete=models.CASCADE)

class NewspaperSheet(SheetModel):
    class Meta:
        verbose_name = _('Newspaper Submission')

    newspaper_name = models.CharField(max_length=255, verbose_name=_('Newspaper'), help_text=_('''Be as specific as possible. If the paper has different regional editions, write in the name of the edition you are monitoring - e.g. 'The Hindu - Delhi edition'.'''))

    page_number = models.PositiveIntegerField(verbose_name=_('(1) Page Number'), help_text=_('Write in the number of the page on which the story begins. Story appears on first page = 1, Seventh page = 7, etc.'))
    topic = field_topic('2')
    scope = field_scope('3')
    space = models.PositiveIntegerField(choices=SPACE, verbose_name=_('(4) Space'))

    equality_rights = field_equality_rights('5')
    about_women = field_about_women('6', _('story'))
    inequality_women = field_inequality_women('7', _('story'))
    stereotypes = field_stereotypes('8', _('story'))
    
    further_analysis = field_further_analysis('24', 'story')
    comments = field_comments('23')

    def __unicode__(self):
        return self.newspaper_name

# ----------------------------
# Radio
# ----------------------------

class RadioPerson(Person):
    sex = field_sex('10')
    occupation = field_occupation('11')
    function = field_function('12')
    family_role = field_family_role('13')
    victim_or_survivor = field_victim_or_survivor('14')
    victim_of = field_victim_of('15')
    survivor_of = field_survivor_of('16')

    special_qn_1 = field_special_qn('17', '1')
    special_qn_2 = field_special_qn('18', '2')
    special_qn_3 = field_special_qn('19', '3')

    radio_sheet = models.ForeignKey('RadioSheet', on_delete=models.CASCADE)

def radio_journalist_meta(name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[1][0],
        'role' : bases[0]._meta.get_fields_with_model()[2][0],
    }
    prepend_verbose(dct, 'role', '8')
    prepend_verbose(dct, 'sex', '9')
    return type(name, bases, mydict)

class RadioJournalist(BroadcastJournalist):
    __metaclass__ = radio_journalist_meta

    radio_sheet = models.ForeignKey('RadioSheet', on_delete=models.CASCADE)

class RadioSheet(SheetModel):
    station_name = models.CharField(max_length=255, verbose_name=_('Name of radio channel or station'), help_text=_('''Be as specific as possible. E.g. if the radio company is called RRI, and if the newscast is broadcast on its third channel, write in 'RRI-3'.'''))

    start_time = models.TimeField(verbose_name=_('Time of Broadcast'))
    num_female_anchors = field_num_female_anchors
    num_male_anchors = field_num_male_anchors

    item_number = field_item_number('1')
    topic = field_topic('2')
    scope = field_scope('3')

    equality_rights = field_equality_rights('4')
    about_women = field_about_women('5', _('story'))
    inequality_women = field_inequality_women('6', _('story'))
    stereotypes = field_stereotypes('7', _('story'))

    further_analysis = field_further_analysis('20', 'story')

    comments = field_comments('N/A')

    def __unicode__(self):
        return self.station_name

    class Meta:
        verbose_name = _('Radio Submission')


# ----------------------------
# Television
# ----------------------------

class TelevisionPerson(Person):
    sex = field_sex('11')
    age = field_age('12')
    occupation = field_occupation('13')
    function = field_function('14')
    family_role = field_family_role('15')
    victim_or_survivor = field_victim_or_survivor('16')
    victim_of = field_victim_of('17')
    survivor_of = field_survivor_of('18')

    special_qn_1 = field_special_qn('19', '1')
    special_qn_2 = field_special_qn('20', '2')
    special_qn_3 = field_special_qn('21', '3')

    television_sheet = models.ForeignKey('TelevisionSheet', on_delete=models.CASCADE)

def television_journalist_meta(name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[0][0],
        'age' : bases[0]._meta.get_fields_with_model()[1][0],
        'role' : bases[0]._meta.get_fields_with_model()[2][0],
    }

    prepend_verbose(dct, 'role', '8')
    prepend_verbose(dct, 'sex', '9')
    prepend_verbose(dct, 'age', '10')
    return type(name, bases, mydict)

class TelevisionJournalist(BroadcastJournalist):
    __metaclass__ = television_journalist_meta

    television_sheet = models.ForeignKey('TelevisionSheet', on_delete=models.CASCADE)

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
    about_women = field_about_women('5', _('story'))
    inequality_women = field_inequality_women('6', _('story'))
    stereotypes = field_stereotypes('7', _('story'))

    further_analysis = field_further_analysis('22', 'story')

    comments = field_comments('N/A')

    def __unicode__(self):
        return self.station_name

    class Meta:
        verbose_name = _('Television Submission')


# ----------------------------
# Internet News
# ----------------------------

def internet_journalist_meta(name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[0][0],
        'age' : bases[0]._meta.get_fields_with_model()[1][0],
    }
    prepend_verbose(dct, 'sex', '10')
    prepend_verbose(dct, 'age', '11')
    return type(name, bases, mydict)

class InternetNewsJournalist(Journalist):
    __metaclass__ = internet_journalist_meta

    internetnews_sheet = models.ForeignKey('InternetNewsSheet', on_delete=models.CASCADE)

class InternetNewsPerson(Person):

    sex = field_sex('12')
    age = field_age('13')
    occupation = field_occupation('14')
    function = field_function('15')
    family_role = field_family_role('16')
    victim_or_survivor = field_victim_or_survivor('17')
    victim_of = field_victim_of('18')
    survivor_of = field_survivor_of('19')
    is_quoted = field_is_quoted('20')
    is_photograph = field_is_photograph('21')

    special_qn_1 = field_special_qn('20', '1')
    special_qn_2 = field_special_qn('21', '2')
    special_qn_3 = field_special_qn('22', '3')

    internetnews_sheet = models.ForeignKey('InternetNewsSheet', on_delete=models.CASCADE)

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
    scope = field_scope('3')
    shared_via_twitter = models.CharField(max_length=1, verbose_name=_('(4) Shared via twitter?'), choices=YESNO, help_text=_('''Has this story been shared by the media house via Twitter?

<br>Enter the exact URL of the story into <a href="https://unionmetrics.com/free-tools/twitter-snapshot-report/" target="_blank">https://unionmetrics.com/free-tools/twitter-snapshot-report/</a> - answer yes if the media house's name appears in the search results.'''))
    shared_on_facebook = models.CharField(max_length=1, choices=YESNO, verbose_name=_('(5) Shared on Facebook'), help_text=_('Has this story been shared by the media house on its Facebook Page?'))
    

    # Analysis
    equality_rights = field_equality_rights('6')
    about_women = field_about_women('7', _('story'))
    inequality_women = field_inequality_women('8', _('story'))
    stereotypes = field_stereotypes('9', 'story')

    further_analysis = field_further_analysis('26', _('story'))

    url_and_multimedia = field_url_and_multimedia('25', 'story')

    def __unicode__(self):
        return self.website_url

    class Meta:
        verbose_name = _('Internet News Submission')

def twitter_journalist_meta(name, bases, mydict):
    dct = {
        'sex' : bases[0]._meta.get_fields_with_model()[0][0],
        'age' : bases[0]._meta.get_fields_with_model()[1][0],
    }
    prepend_verbose(dct, 'sex', '7')
    prepend_verbose(dct, 'age', '8')
    return type(name, bases, mydict)

# ----------------------------
# Twitter
# ----------------------------

class TwitterJournalist(Journalist):
    __metaclass__ = twitter_journalist_meta

    twitter_sheet = models.ForeignKey('TwitterSheet', on_delete=models.CASCADE)

class TwitterPerson(Person):
    sex = field_sex('9')
    age = field_age('10')
    occupation = field_occupation('11')
    function = field_function('12')
    is_photograph = field_is_photograph('13')

    special_qn_1 = field_special_qn('14', '1')
    special_qn_2 = field_special_qn('15', '2')
    special_qn_3 = field_special_qn('16', '3')

    twitter_sheet = models.ForeignKey('TwitterSheet', on_delete=models.CASCADE)

class TwitterSheet(SheetModel):
    class Meta:
        verbose_name = _('Twitter Submission')

    media_name = models.CharField(max_length=255, verbose_name=_('Media Name'), help_text=_('''For example. 'CNN Breaking News' '''))
    twitter_handle = models.CharField(max_length=255, verbose_name=_('Twitter Handle'), help_text=_('e.g. @cnnbrk'))

    # Story
    retweet = models.PositiveIntegerField(choices=RETWEET,
        verbose_name=_('(1) Tweet or Retweet'),
        help_text=_('Only retweets from the same media house can be coded. Do not code retweets from other news providers')
    )
    topic = field_topic('2')
    
    # Analysis
    equality_rights = field_equality_rights('3')
    about_women = field_about_women('4', _('story'))
    inequality_women = field_inequality_women('5', _('story'))
    stereotypes = field_stereotypes('6', 'story')

    further_analysis = field_further_analysis('18', _('tweet'))

    url_and_multimedia = field_url_and_multimedia('17', 'tweet')

    def __unicode__(self):
        return self.twitter_handle


sheet_models = OrderedDict([
    ('Print', NewspaperSheet),
    ('Radio', RadioSheet),
    ('Television', TelevisionSheet),
    ('Internet', InternetNewsSheet),
    ('Twitter', TwitterSheet)
])

tm_sheet_models = OrderedDict([
    ('Print', NewspaperSheet),
    ('Radio', RadioSheet),
    ('Television', TelevisionSheet)
])

dm_sheet_models = OrderedDict([
    ('Internet', InternetNewsSheet),
    ('Twitter', TwitterSheet)
])

person_models = OrderedDict([
    ('Print', NewspaperPerson),
    ('Radio', RadioPerson),
    ('Television', TelevisionPerson),
    ('Internet', InternetNewsPerson),
    ('Twitter', TwitterPerson)]
)

tm_person_models = OrderedDict([
    ('Print', NewspaperPerson),
    ('Radio', RadioPerson),
    ('Television', TelevisionPerson),
])

dm_person_models = OrderedDict([
    ('Internet', InternetNewsPerson),
    ('Twitter', TwitterPerson)
])

journalist_models = OrderedDict([
    ('Print', NewspaperJournalist),
    ('Radio', RadioJournalist),
    ('Television', TelevisionJournalist),
    ('Internet', InternetNewsJournalist),
    ('Twitter', TwitterJournalist)
])

tm_journalist_models = OrderedDict([
    ('Print', NewspaperJournalist),
    ('Radio', RadioJournalist),
    ('Television', TelevisionJournalist),
])

broadcast_journalist_models = OrderedDict([
    ('Radio', RadioJournalist),
    ('Television', TelevisionJournalist),
])

dm_journalist_models = OrderedDict([
    ('Internet', InternetNewsJournalist),
    ('Twitter', TwitterJournalist)
])

all_models = OrderedDict([
    ('Sheets', sheet_models),
    ('Sources', person_models),
    ('Reporters', journalist_models)
])
