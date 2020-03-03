from collections import OrderedDict

from django.db import models
from django.utils.translation import gettext_lazy as _

from forms.modelutils import *

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
    sex = field_sex(_('(10) Sex'))
    age = field_age(_('(11) Age (person appears)'))
    occupation = field_occupation(_('(12) Occupation or Position'))
    function = field_function(_('(13) Function in the news story'))
    family_role = field_family_role(_('(14) Family Role Given?'))
    victim_or_survivor = field_victim_or_survivor(_('(15) Does the story identify the person as either a victim or survivor?'))
    victim_of = field_victim_of(_('(16) The story identifies the person as a victim of:'))
    survivor_of = field_survivor_of(_('(17) The story identifies the person as a survivor of:'))
    is_quoted = field_is_quoted(_('(18) Is the person directly quoted'))
    is_photograph = field_is_photograph(_('(19) Is there a photograph of the person in the story?'))

    special_qn_1 = field_special_qn(_('(20) Special question (1)'))
    special_qn_2 = field_special_qn(_('(21) Special question (2)'))
    special_qn_3 = field_special_qn(_('(22) Special question (3)'))

    newspaper_sheet = models.ForeignKey('NewspaperSheet', on_delete=models.CASCADE)

class NewspaperSheet(SheetModel):
    class Meta:
        verbose_name = _('Newspaper')

    newspaper_name = models.CharField(max_length=255, verbose_name=_('Newspaper'), help_text=_('''Be as specific as possible. If the paper has different regional editions, write in the name of the edition you are monitoring - e.g. 'The Hindu - Delhi edition'.'''))

    page_number = models.PositiveIntegerField(verbose_name=_('(1) Page Number'), help_text=_('Write in the number of the page on which the story begins. Story appears on first page = 1, Seventh page = 7, etc.'))
    topic = field_topic(_('(2) Topic'))
    scope = field_scope(_('(3) Scope'))
    space = models.PositiveIntegerField(choices=SPACE, verbose_name=_('(4) Space'))

    equality_rights = field_equality_rights(_('(5) Reference to gender equality / human rights legislation/ policy'))
    about_women = field_about_women(_('(6) Is the story about a particular woman or group of women?'))
    inequality_women = field_inequality_women(_('(7) This story clearly highlights issues of inequality between women and men'))
    stereotypes = field_stereotypes(_('(8) This story clearly challenges gender stereotypes'))

    further_analysis = field_further_analysis(_('(24) Does this story warrant further analysis?'), _('''<br><br>A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation'''))
    comments = field_comments(_('(23) Describe any photographs included in the story and the conclusions you draw from them.'))

    def __str__(self):
        return self.newspaper_name

# ----------------------------
# Radio
# ----------------------------

class RadioPerson(Person):
    sex = field_sex(_('(10) Sex'))
    occupation = field_occupation(_('(11) Occupation or Position'))
    function = field_function(_('(12) Function in the news story'))
    family_role = field_family_role(_('(13) Family Role Given?'))
    victim_or_survivor = field_victim_or_survivor(_('(14) Does the story identify the person as either a victim or survivor?'))
    victim_of = field_victim_of(_('(15) The story identifies the person as a victim of:'))
    survivor_of = field_survivor_of(_('(16) The story identifies the person as a survivor of:'))

    special_qn_1 = field_special_qn(_('(17) Special question (1)'))
    special_qn_2 = field_special_qn(_('(18) Special question (2)'))
    special_qn_3 = field_special_qn(_('(19) Special question (3)'))

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
    channel = models.CharField(max_length=255, verbose_name=_('Channel'), help_text=_('''Be as specific as possible. E.g. if the radio company is called RRI, and if the newscast is broadcast on its third channel, write in 'RRI-3'.'''))

    start_time = models.TimeField(verbose_name=_('Time of Broadcast'))
    num_female_anchors = field_num_female_anchors
    num_male_anchors = field_num_male_anchors

    item_number = field_item_number(_('(1) Item Number'))
    topic = field_topic(_('(2) Topic'))
    scope = field_scope(_('(3) Scope'))

    equality_rights = field_equality_rights(_('(4) Reference to gender equality / human rights legislation/ policy'))
    about_women = field_about_women(_('(5) Is the story about a particular woman or group of women?'))
    inequality_women = field_inequality_women(_('(6) This story clearly highlights issues of inequality between women and men'))
    stereotypes = field_stereotypes(_('(7) This story clearly challenges gender stereotypes'))

    further_analysis = field_further_analysis(_('(20) Does this story warrant further analysis?'), _('''<br><br>A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation'''))

    comments = field_comments(_('(N/A) Describe any photographs included in the story and the conclusions you draw from them.'))

    def __str__(self):
        return self.channel

    class Meta:
        verbose_name = _('Radio')


# ----------------------------
# Television
# ----------------------------

class TelevisionPerson(Person):
    sex = field_sex(_('(11) Sex'))
    age = field_age(_('(12) Age (person appears)'))
    occupation = field_occupation(_('(13) Occupation or Position'))
    function = field_function(_('(14) Function in the news story'))
    family_role = field_family_role(_('(15) Family Role Given?'))
    victim_or_survivor = field_victim_or_survivor(_('(16) Does the story identify the person as either a victim or survivor?'))
    victim_of = field_victim_of(_('(17) The story identifies the person as a victim of:'))
    survivor_of = field_survivor_of(_('(18) The story identifies the person as a survivor of:'))

    special_qn_1 = field_special_qn(_('(19) Special question (1)'))
    special_qn_2 = field_special_qn(_('(20) Special question (2)'))
    special_qn_3 = field_special_qn(_('(21) Special question (3)'))

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
    channel = models.CharField(max_length=255, verbose_name=_('Channel'), help_text=_('''Be as specific as possible. E.g. if the television company is called RTV, and if the newscast is broadcast on its second channel, write in 'RTV-2' '''))
    start_time = models.TimeField(verbose_name=_('Time of Broadcast'))
    num_female_anchors = field_num_female_anchors
    num_male_anchors = field_num_male_anchors

    item_number = field_item_number(_('(1) Item Number'))
    topic = field_topic(_('(2) Topic'))
    scope = field_scope(_('(3) Scope'))

    equality_rights = field_equality_rights(_('(4) Reference to gender equality / human rights legislation/ policy'))
    about_women = field_about_women(_('(5) Is the story about a particular woman or group of women?'))
    inequality_women = field_inequality_women(_('(6) This story clearly highlights issues of inequality between women and men'))
    stereotypes = field_stereotypes(_('(7) This story clearly challenges gender stereotypes'))

    further_analysis = field_further_analysis(_('(22) Does this story warrant further analysis?'), _('''<br><br>A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation'''))

    comments = field_comments(_('(N/A) Describe any photographs included in the story and the conclusions you draw from them.'))

    def __str__(self):
        return self.channel

    class Meta:
        verbose_name = _('Television')


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

    sex = field_sex(_('(12) Sex'))
    age = field_age(_('(13) Age (person appears)'))
    occupation = field_occupation(_('(14) Occupation or Position'))
    function = field_function(_('(15) Function in the news story'))
    family_role = field_family_role(_('(16) Family Role Given?'))
    victim_or_survivor = field_victim_or_survivor(_('(17) Does the story identify the person as either a victim or survivor?'))
    victim_of = field_victim_of(_('(18) The story identifies the person as a victim of:'))
    survivor_of = field_survivor_of(_('(19) The story identifies the person as a survivor of:'))
    is_quoted = field_is_quoted(_('(20) Is the person directly quoted'))
    is_photograph = field_is_photograph(_('(21) Is there a photograph of the person in the story?'))

    special_qn_1 = field_special_qn(_('(22) Special question (1)'))
    special_qn_2 = field_special_qn(_('(23) Special question (2)'))
    special_qn_3 = field_special_qn(_('(24) Special question (3)'))

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
    topic = field_topic(_('(2) Topic'))
    scope = field_scope(_('(3) Scope'))
    shared_via_twitter = models.CharField(max_length=1, verbose_name=_('(4) Shared via twitter?'), choices=YESNO, help_text=_('''Has this story been shared by the media house via Twitter?

<br>Enter the exact URL of the story into <a href="https://twitter.com" target="_blank">https://twitter.com</a> - answer yes if the media house's name appears in the search results.'''))
    shared_on_facebook = models.CharField(max_length=1, choices=YESNO, verbose_name=_('(5) Shared on Facebook'), help_text=_('''Has this story been shared by the media house on its Facebook Page?

<br>Scroll down the media house's Facebook page to check.'''))

    # Analysis
    equality_rights = field_equality_rights(_('(6) Reference to gender equality / human rights legislation/ policy'))
    about_women = field_about_women(_('(7) Is the story about a particular woman or group of women?'))
    inequality_women = field_inequality_women(_('(8) This story clearly highlights issues of inequality between women and men'))
    stereotypes = field_stereotypes(_('(9) This story clearly challenges gender stereotypes'))

    further_analysis = field_further_analysis(_('(26) Does this story warrant further analysis?'), _('''<br><br>A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation'''))

    url_and_multimedia = field_url_and_multimedia(_('(25) Copy and paste the URL of the story. Describe any photographs, images, other multimedia features included in the story. Note down the conclusions you draw from the images, audio and video.'))

    def __str__(self):
        return self.website_url

    class Meta:
        verbose_name = _('Internet')

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
    sex = field_sex(_('(9) Sex'))
    age = field_age(_('(10) Age (person appears)'))
    occupation = field_occupation(_('(11) Occupation or Position'))
    function = field_function(_('(12) Function in the news story'))
    is_photograph = field_is_photograph(_('(13) Is there a photograph of the person in the story?'))

    special_qn_1 = field_special_qn(_('(14) Special question (1)'))
    special_qn_2 = field_special_qn(_('(15) Special question (2)'))
    special_qn_3 = field_special_qn(_('(16) Special question (3)'))

    twitter_sheet = models.ForeignKey('TwitterSheet', on_delete=models.CASCADE)

class TwitterSheet(SheetModel):
    class Meta:
        verbose_name = _('Twitter')

    media_name = models.CharField(max_length=255, verbose_name=_('Media Name'), help_text=_('''For example. 'CNN Breaking News' '''))
    twitter_handle = models.CharField(max_length=255, verbose_name=_('Twitter Handle'), help_text=_('e.g. @cnnbrk'))

    # Story
    retweet = models.PositiveIntegerField(choices=RETWEET,
        verbose_name=_('(1) Tweet or Retweet'),
        help_text=_('Only retweets from the same media house can be coded. Do not code retweets from other news providers')
    )
    topic = field_topic(_('(2) Topic'))

    # Analysis
    equality_rights = field_equality_rights(_('(3) Reference to gender equality / human rights legislation/ policy'))
    about_women = field_about_women(_('(4) Is the story about a particular woman or group of women?'))
    inequality_women = field_inequality_women(_('(5) This story clearly highlights issues of inequality between women and men'))
    stereotypes = field_stereotypes(_('(6) This story clearly challenges gender stereotypes'))

    further_analysis = field_further_analysis(_('(18) Does this tweet warrant further analysis?'), _('''<br><br>A tweet warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation'''))

    url_and_multimedia = field_url_and_multimedia(_('(17) Copy and paste the URL of the tweet. Describe any photographs, images, other multimedia features included in the tweet. Note down the conclusions you draw from the images, audio and video.'))

    def __str__(self):
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
