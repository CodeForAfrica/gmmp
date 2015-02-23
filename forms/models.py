from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

WEB_LAYER = zip(range(1, 10), range(1, 10))
TOPICS = (
    (1,  _('Women politicians, women electoral candidates...')),
    (2,  _('Peace, negotiations, treaties')),
    (3,  _('Other domestic politics, government, etc.')),
    (4,  _('Global partnerships')),
    (5,  _('Foreign/international politics, UN, peacekeeping')),
    (6,  _('National defence, military spending, internal security, etc.')),
    (7,  _('Other stories on politics (specify in comments)')),
    (8,  _('Economic policies, strategies, modules, indicators, stock markets, etc')),
    (9,  _('Economic crisis, state bailouts of companies, company takeovers and mergers, etc.')),
    (10, _('Poverty, housing, social welfare, aid, etc.')),
    (11, _('Women''s participation in economic processes')),
    (12, _('Employment')),
    (13, _('Informal work, street vending, etc.')),
    (14, _('Other labour issues (strikes, trade unions, etc.)')),
    (15, _('Rural economy, agriculture, farming, land rights')),
    (16, _('Consumer issues, consumer protection, fraud...')),
    (17, _('Transport, traffic, roads...')),
    (18, _('Other stories on economy (specify in comments)')),
    (19, _('Science, technology, research, discoveries...')),
    (20, _('Medicine, health, hygiene, safety, (not EBOLA or HIV/AIDS)')),
    (21, _('EBOLA, treatment, response...')),
    (22, _('HIV and AIDS, policy, treatment, etc')),
    (23, _('Other epidemics, viruses, contagions, Influenza, BSE, SARS')),
    (24, _('Birth control, fertility, sterilization, termination...')),
    (25, _('Climate change, global warming')),
    (26, _('Environment, pollution, tourism')),
    (27, _('Other stories on science (specify in comments)')),
    (28, _('Millennium Development Goals (MDGs), Post 2015 agenda, Sustainable Development Goals')),
    (29, _('Family relations, inter-generational conflict, parents')),
    (30, _('Human rights, women''s rights, rights of sexual minorities, rights of religious minorities, etc.')),
    (31, _('Religion, culture, tradition, controversies...')),
    (32, _('Migration, refugees, xenophobia, ethnic conflict...')),
    (33, _('Other development issues, sustainability, etc.')),
    (34, _('Education, childcare, nursery, university, literacy')),
    (35, _('Women''s movement, activism, demonstrations, etc')),
    (36, _('Changing gender relations (outside the home)')),
    (37, _('Family law, family codes, property law, inheritance...')),
    (38, _('Legal system, judiciary, legislation apart from family')),
    (39, _('Disaster, accident, famine, flood, plane crash, etc.')),
    (40, _('Riots, demonstrations, public disorder, etc.')),
    (41, _('Other stories on social/legal (specify in comments)')),
    (42, _('Non-violent crime, bribery, theft, drugs, corruption')),
    (43, _('Violent crime, murder, abduction, assault, etc.')),
    (44, _('Gender violence based on culture, family, inter-personal relations, feminicide, harassment, rape, sexual assault, trafficking, FGM...')),
    (45, _('Gender violence perpetuated by the State')),
    (46, _('Child abuse, sexual violence against children, neglect')),
    (47, _('War, civil war, terrorism, other state-based violence')),
    (48, _('Other crime/violence (specify in comments)')),
    (49, _('Celebrity news, births, marriages, royalty, etc.')),
    (50, _('Arts, entertainment, leisure, cinema, books, dance')),
    (51, _('Media, (including internet), portrayal of women/men')),
    (52, _('Beauty contests, models, fashion, cosmetic surgery')),
    (53, _('Sports, events, players, facilities, training, funding')),
    (54, _('Other celebrity/arts/media news (specify in comments)')),
    (55, _('Other (only use as a last resort & explain)')),
)

SCOPE = (
    (1, _('Local')),
    (2, _('National')),
    (3, _('Sub-Regional')),
    (4, _('Foreign/International')),
)

YESNO = (
    ('Y', _('Yes')),
    ('N', _('No')),
)

GENDER = (
    (1, _('Male')),
    (2, _('Female')),
    (3, _('Other (transgender, etc.)')),
    (4, _('Do not know')),
)

AGES = (
    (0, _('Do not know')),
    (1, _('12 and under')),
    (2, _('13-18')),
    (3, _('19-34')),
    (4, _('35-49')),
    (5, _('50-64')),
    (6, _('65 years or more')),
)

SOURCE = (
    (1, _('Person')),
    (2, _('Secondary Source')),
)

OCCUPATION = [
    (0,  _('Not stated')),
    (1,  _('Royalty, monarch, deposed monarch, etc.')),
    (2,  _('Government, politician, minister, spokesperson...')),
    (3,  _('Government employee, public servant, etc.')),
    (4,  _('Police, military, para-military, militia, fire officer')),
    (5,  _('Academic expert, lecturer, teacher')),
    (6,  _('Doctor, dentist, health specialist')),
    (7,  _('Health worker, social worker, childcare worker')),
    (8,  _('Science/ technology professional, engineer, etc.')),
    (9,  _('Media professional, journalist, film-maker, etc.')),
    (10, _('Lawyer, judge, magistrate, legal advocate, etc.')),
    (11, _('Business person, exec, manager, stock broker...')),
    (12, _('Office or service worker, non-management worker')),
    (13, _('Tradesperson, artisan, labourer, truck driver, etc.')),
    (14, _('Agriculture, mining, fishing, forestry')),
    (15, _('Religious figure, priest, monk, rabbi, mullah, nun')),
    (16, _('Activist or worker in civil society org., NGO, trade union')),
    (17, _('Sex worker')),
    (18, _('Celebrity, artist, actor, writer, singer, TV personality')),
    (19, _('Sportsperson, athlete, player, coach, referee')),
    (20, _('Student, pupil, schoolchild')),
    (21, _('Homemaker, parent (male or female)) only if no other occupation is given e.g. doctor/mother=code 6')),
    (22, _('Child, young person no other occupation given')),
    (23, _('Villager or resident no other occupation given')),
    (24, _('Retired person, pensioner no other occupation given')),
    (25, _('Criminal, suspect no other occupation given')),
    (26, _('Unemployed no other occupation given')),
    (27, _('Other only as last resort & explain')),
]

FUNCTION = [
    (0, _('Do not know')),
    (1, _('Subject')),
    (2, _('Spokesperson')),
    (3, _('Expert or commentator')),
    (4, _('Personal Experience')),
    (5, _('Eye Witness')),
    (6, _('Popular Opinion')),
    (7, _('Other')),
]

VICTIM_OF = [
    (0, _('Not applicable (the story identifies the person only as a survivor)')),
    (1, _('Victim of an accident, natural disaster, poverty')),
    (2, _('Victim of domestic violence, rape, murder, etc.')),
    (3, _('Victim of non-domestic sexual violence, rape, assault, etc (sexual violence only)')),
    (4, _('Victim of other non-domestic crime, robbery, etc.')),
    (5, _('Victim of violation based on religion, tradition...')),
    (6, _('Victim of war, terrorism, vigilantism, state violence...')),
    (7, _('Victim of discrimination based on gender, race, ethnicity, age, religion, ability, etc')),
    (8, _('Other victim (specify in comments)')),
    (9, _('Do not know, cannot decide')),
]

SURVIVOR_OF = [
    (0, _('Not applicable (the story identifies the person only as a victim)')),
    (1, _('Survivor of an accident, natural disaster, poverty')),
    (2, _('Survivor of domestic violence, rape, murder, etc.')),
    (3, _('Survivor of non-domestic sexual violence, rape, assault, etc. (sexual violence only)')),
    (4, _('Survivor of other non-domestic crime, robbery, etc.')),
    (5, _('Survivor of violation based on religion, tradition...')),
    (6, _('Survivor of war, terrorism, vigilantism, state violence...')),
    (7, _('Survivor of discrimination based on gender, race, ethnicity, age, religion, ability, etc.')),
    (8, _('Other survivor (specify in comments)')),
    (9, _('Do not know, cannot decide')),
]

IS_PHOTOGRAPH = [
    (1, _('Yes')),
    (2, _('No')),
    (3, _('Do not know')),
]

AGREE_DISAGREE = [
    (1, _('Agree')),
    (2, _('Disagree')),
    (3, _('Neither agree nor disagree')),
    (4, _('Do not know')),
]

RETWEET = [
    (1, _('Tweet')),
    (2, _('Retweet')),
]

class InternetNewsJournalist(models.Model):
    # Journalists / Reporters
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Journalist''s Sex'))
    age = models.PositiveIntegerField(choices=AGES, verbose_name=_('Age (person appears)'))
    internet_news_sheet = models.ForeignKey('InternetNewsSheet')
    tbl = dict(GENDER)

    def __unicode__(self):
        return u"%s (%d)" % (self.tbl[self.sex], self.age)

class TwitterJournalist(models.Model):
    # Journalists / Reporters
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Journalist''s Sex'))
    tbl = dict(GENDER)
    twitter_sheet = models.OneToOneField('TwitterSheet')

    def __unicode__(self):
        return u"%s" % (self.tbl[self.sex])

class Person(models.Model):
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

class TwitterPerson(models.Model):
    # Setting the unicode to blank in the admin
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Sex'))
    is_photograph = models.PositiveIntegerField(choices=IS_PHOTOGRAPH, verbose_name=_('Photo/Video of person attached'))
    twitter_sheet = models.ForeignKey('TwitterSheet')

class SheetModel(models.Model):
    monitor = models.ForeignKey(User, null=False)

    class Meta:
        abstract = True

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
    topic = models.PositiveIntegerField(choices=TOPICS, help_text=_('''Within each broad category, we include a code for 'other stories'. Please use these codes only as a last resort.'''), verbose_name=_('Topic'))
    comments = models.TextField(verbose_name=_('Describe any photographs, images, other multimedia components included in the tweet and the conclusions you draw from them.'), blank=True)
    url_and_multimedia = models.TextField(verbose_name=_('Copy and paste the URL of the story. Describe any photographs, images, other multimedia features included in the story. Note down the conclusions you draw from the images, audio and video..'), blank=True)

    # Analysis
    about_women = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Is the story about a particular woman or group of women?'))
    stereotypes = models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=_('This story clearly challenges gender stereotypes'))
    further_analysis = models.CharField(max_length=1, choices=YESNO, verbose_name=_('Does this tweet warrant further analysis?'), help_text=_('<br><br>A tweet warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it presents the story being tweeted in a sensationalist, gender-biased manner, etc . Consult the guide for further explanation<br>If you select Yes, you will need to send a print-out of the tweet and screen grab of the page to your national/regional coordinator.'))
