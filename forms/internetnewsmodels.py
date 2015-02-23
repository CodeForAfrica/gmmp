from django.db import models
from django.utils.translation import ugettext_lazy as _
from modelutils import *

class InternetNewsJournalist(models.Model):
    # Journalists / Reporters
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Journalist''s Sex'))
    age = models.PositiveIntegerField(choices=AGES, verbose_name=_('Age (person appears)'))
    internet_news_sheet = models.ForeignKey('InternetNewsSheet')
    tbl = dict(GENDER)

    def __unicode__(self):
        return u"%s (%d)" % (self.tbl[self.sex], self.age)

class InternetNewsPerson(models.Model):
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Sex'))
    age = models.PositiveIntegerField(choices=AGES, verbose_name=_('Age (person appears)'))
    occupation = models.PositiveIntegerField(choices=OCCUPATION, verbose_name=_('Occupation or Position'))
    occupation_other = models.TextField(verbose_name=_('Other Occupation'), blank=True)
    function = models.PositiveIntegerField(choices=FUNCTION, verbose_name=_('Function in the news story'))
    # TODO - need more information here
    family_role = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Family Role Given.'), help_text=_('''Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.'''))
    victim_or_survivor = models.CharField(max_length=1, choices=YESNO, 
        verbose_name=_('Does the story identify the person as either a victim or survivor?'),
        help_text=_('''<p>You should code a person as a <strong>victim</strong> either if the word 'victim' is used to describe her/him, or if the story Implies that the person is a victim - e.g. by using language or images that evoke particular emotions such as shock, horror, pity for the person.</p><p>You should code a person as a <strong>survivor</strong> either if the word 'survivor' is used to describe her/him, or if the story implies that the person is a survivor - e.g. by using language or images that evoke particular emotions such as admiration or respect for the person.</p>''')
        )

    # TODO - hide this if no to the previous question
    victim_of = models.PositiveIntegerField(choices=VICTIM_OF, verbose_name=_('The story identifies the person as a victim of:'))
    victim_comments = models.TextField(verbose_name=_('Add comments if ''Other Victim'' was selected above'), blank=True)

    # TODO - hide this if no to the previous question
    survivor_of = models.PositiveIntegerField(choices=SURVIVOR_OF, verbose_name=_('The story identifies the person as a survivor of:'))
    survivor_comments = models.TextField(verbose_name=_('Add comments if ''Other Survivor'' was selected above'), blank=True)
    is_quoted = models.CharField(max_length=1, choices=YESNO, 
        verbose_name=_('Is the person directly quoted'), 
        help_text=_('<p>A person is <strong>directly quoted</strong> if their own words are printed, e.g. "The war against terror is our first priority" said President Bush.</p><p>If the story paraphrases what the person said, that is not a direct quote, e.g. President Bush said that top priority would be given to fighting the war against terror.</p>')
    )
    is_photograph = models.PositiveIntegerField(choices=IS_PHOTOGRAPH, verbose_name=_('Is there a photograph of the person in the story?'))

    internet_news_sheet = models.ForeignKey('InternetNewsSheet')

    class Meta:
        verbose_name = _('Person')

class InternetNewsSheet(SheetModel):
    # Story
    website_name = models.CharField(max_length=255, verbose_name=_('Website Name'))
    website_url = models.CharField(max_length=255, verbose_name=_('URL'))
    time_accessed = models.DateTimeField(verbose_name=_('Date and Time Accessed'))
    offline_presence = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Offline presence?'))
    
    webpage_layer_no = models.PositiveIntegerField(choices=WEB_LAYER, help_text=_('Webpage Layer Number. Homepage=1, One click away=2, Five clicks away= 5, etc. Note that if a story appears on the front page, code with 1'), verbose_name=_('Webpage Layer Number'))
    topic = models.PositiveIntegerField(choices=TOPICS, help_text=_('Topic'), verbose_name=_('Topic'))
    topic_comments = models.TextField(verbose_name=_('Topic Comments'), help_text=_('Complete if no topic above is applicable'), blank=True)
    scope = models.PositiveIntegerField(choices=SCOPE, verbose_name=_('Scope'))
    shared_via_twitter = models.CharField(max_length=1, choices=YESNO, help_text=_('''Has this story been shared by the media house via Twitter?

<br>Enter the exact URL of the story into <a href="http://topsy.com/" target="_blank">http://topsy.com</a> - answer yes if the media house's name appears in the search results.'''), verbose_name=_('Shared via Twitter'))
    shared_on_facebook = models.CharField(max_length=1, choices=YESNO, help_text=_('Has this story been shared by the media house on its Facebook Page?'), verbose_name=_('Shared on Facebook'))
    equality_rights = models.CharField(max_length=1, choices=YESNO, help_text=_('Reference to gender equality/ human rights legislation/ policy?'), verbose_name=_('Equality Rights'))

    # Source
    person_secondary = models.PositiveIntegerField(choices=SOURCE, verbose_name=_('Source'), help_text=_('''<br><br>
    Select ''Secondary Source'' only if the story is based solely on information from a report, article, or other piece of written information.<br><br>
<strong>Code information for:</strong><br>
  - Any person whom the story is about even if they are not interviewed or quoted<br>
  - Each person who is interviewed<br>
  - Each person in the story who is quoted, either directly or indirectly. Code only individual people.<br>
<br>
<strong>Do not code:</strong>
  - Groups (e.g. a group of nurses, a group of soldiers);</br>
  - Organisations, companies, collectivities (e.g. political parties);</br>
  - Characters in novels or movies (unless the story is about them);</br>
  - Deceased historical figures (unless the story is about them);</br>
  - Interpreters (Code the person being interviewed as if they spoke without an interpreter).</br>
'''))

    # Analysis
    about_women = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Is the story about a particular woman or group of women?'))
    inequality_women = models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=_('This story clearly highlights issues of inequality between women and men'))
    stereotypes = models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=_('This story clearly challenges gender stereotypes'))
    further_analysis = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Does this story warrant further analysis?'), help_text=_('<br><br>A story warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women''s opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women''s human rights, etc. Consult the guide for further explanation'))
    url_and_multimedia = models.TextField(verbose_name=_('Copy and paste the URL of the story. Describe any photographs, images, other multimedia features included in the story. Note down the conclusions you draw from the images, audio and video..'), blank=True)
    comments = models.TextField(verbose_name=_('Describe any photographs included in the story and the conclusions you draw from them.'), blank=True)

    def __unicode__(self):
        return self.website_url

    class Meta:
        verbose_name = _('Internet News Submission')

