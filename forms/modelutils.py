from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django_countries.fields import CountryField

from gmmp.models import Monitor


TOPICS = (
    (1,  _('(1) Women politicians, women electoral candidates...')),
    (2,  _('(2) Peace, negotiations, treaties')),
    (3,  _('(3) Other domestic politics, government, etc.')),
    (4,  _('(4) Global partnerships')),
    (5,  _('(5) Foreign/international politics, UN, peacekeeping')),
    (6,  _('(6) National defence, military spending, internal security, etc.')),
    (7,  _('(7) Other stories on politics (specify in comments)')),
    (8,  _('(8) Economic policies, strategies, modules, indicators, stock markets, etc')),
    (9,  _('(9) Economic crisis, state bailouts of companies, company takeovers and mergers, etc.')),
    (10, _('(10) Poverty, housing, social welfare, aid, etc.')),
    (11, _('(11) Women''s participation in economic processes')),
    (12, _('(12) Employment')),
    (13, _('(13) Informal work, street vending, etc.')),
    (14, _('(14) Other labour issues (strikes, trade unions, etc.)')),
    (15, _('(15) Rural economy, agriculture, farming, land rights')),
    (16, _('(16) Consumer issues, consumer protection, fraud...')),
    (17, _('(17) Transport, traffic, roads...')),
    (18, _('(18) Other stories on economy (specify in comments)')),
    (19, _('(19) Science, technology, research, discoveries...')),
    (20, _('(20) Medicine, health, hygiene, safety, (not EBOLA or HIV/AIDS)')),
    (21, _('(21) EBOLA, treatment, response...')),
    (22, _('(22) HIV and AIDS, policy, treatment, etc')),
    (23, _('(23) Other epidemics, viruses, contagions, Influenza, BSE, SARS')),
    (24, _('(24) Birth control, fertility, sterilization, termination...')),
    (25, _('(25) Climate change, global warming')),
    (26, _('(26) Environment, pollution, tourism')),
    (27, _('(27) Other stories on science (specify in comments)')),
    (28, _('(28) Millennium Development Goals (MDGs), Post 2015 agenda, Sustainable Development Goals')),
    (29, _('(29) Family relations, inter-generational conflict, parents')),
    (30, _('(30) Human rights, women''s rights, rights of sexual minorities, rights of religious minorities, etc.')),
    (31, _('(31) Religion, culture, tradition, controversies...')),
    (32, _('(32) Migration, refugees, xenophobia, ethnic conflict...')),
    (33, _('(33) Other development issues, sustainability, etc.')),
    (34, _('(34) Education, childcare, nursery, university, literacy')),
    (35, _('(35) Women''s movement, activism, demonstrations, etc')),
    (36, _('(36) Changing gender relations (outside the home)')),
    (37, _('(37) Family law, family codes, property law, inheritance...')),
    (38, _('(38) Legal system, judiciary, legislation apart from family')),
    (39, _('(39) Disaster, accident, famine, flood, plane crash, etc.')),
    (40, _('(40) Riots, demonstrations, public disorder, etc.')),
    (41, _('(41) Other stories on social/legal (specify in comments)')),
    (42, _('(42) Non-violent crime, bribery, theft, drugs, corruption')),
    (43, _('(43) Violent crime, murder, abduction, assault, etc.')),
    (44, _('(44) Gender violence based on culture, family, inter-personal relations, feminicide, harassment, rape, sexual assault, trafficking, FGM...')),
    (45, _('(45) Gender violence perpetuated by the State')),
    (46, _('(46) Child abuse, sexual violence against children, neglect')),
    (47, _('(47) War, civil war, terrorism, other state-based violence')),
    (48, _('(48) Other crime/violence (specify in comments)')),
    (49, _('(49) Celebrity news, births, marriages, royalty, etc.')),
    (50, _('(50) Arts, entertainment, leisure, cinema, books, dance')),
    (51, _('(51) Media, (including internet), portrayal of women/men')),
    (52, _('(52) Beauty contests, models, fashion, cosmetic surgery')),
    (53, _('(53) Sports, events, players, facilities, training, funding')),
    (54, _('(54) Other celebrity/arts/media news (specify in comments)')),
    (55, _('(55) Other (only use as a last resort & explain)')),
)

SCOPE = (
    (1, _('(1) Local')),
    (2, _('(2) National')),
    (3, _('(3) Sub-Regional')),
    (4, _('(4) Foreign/International')),
)

YESNO = (
    ('Y', _('(1) Yes')),
    ('N', _('(2) No')),
)

GENDER = (
    (1, _('(1) Female')),
    (2, _('(2) Male')),
    (3, _('(3) Other (transgender, etc.)')),
    (4, _('(4) Do not know')),
)

AGES = (
    (0, _('(0) Do not know')),
    (1, _('(1) 12 and under')),
    (2, _('(2) 13-18')),
    (3, _('(3) 19-34')),
    (4, _('(4) 35-49')),
    (5, _('(5) 50-64')),
    (6, _('(6) 65 years or more')),
)

SOURCE = (
    (0, _('(0) Do not know')),
    (1, _('(1) Person')),
    (2, _('(2) Secondary Source')),
)

OCCUPATION = [
    (0,  _('(0) Not stated')),
    (1,  _('(1) Royalty, monarch, deposed monarch, etc.')),
    (2,  _('(2) Government, politician, minister, spokesperson...')),
    (3,  _('(3) Government employee, public servant, etc.')),
    (4,  _('(4) Police, military, para-military, militia, fire officer')),
    (5,  _('(5) Academic expert, lecturer, teacher')),
    (6,  _('(6) Doctor, dentist, health specialist')),
    (7,  _('(7) Health worker, social worker, childcare worker')),
    (8,  _('(8) Science/ technology professional, engineer, etc.')),
    (9,  _('(9) Media professional, journalist, film-maker, etc.')),
    (10, _('(10) Lawyer, judge, magistrate, legal advocate, etc.')),
    (11, _('(11) Business person, exec, manager, stock broker...')),
    (12, _('(12) Office or service worker, non-management worker')),
    (13, _('(13) Tradesperson, artisan, labourer, truck driver, etc.')),
    (14, _('(14) Agriculture, mining, fishing, forestry')),
    (15, _('(15) Religious figure, priest, monk, rabbi, mullah, nun')),
    (16, _('(16) Activist or worker in civil society org., NGO, trade union')),
    (17, _('(17) Sex worker')),
    (18, _('(18) Celebrity, artist, actor, writer, singer, TV personality')),
    (19, _('(19) Sportsperson, athlete, player, coach, referee')),
    (20, _('(20) Student, pupil, schoolchild')),
    (21, _('(21) Homemaker, parent (male or female)) only if no other occupation is given e.g. doctor/mother=code 6')),
    (22, _('(22) Child, young person no other occupation given')),
    (23, _('(23) Villager or resident no other occupation given')),
    (24, _('(24) Retired person, pensioner no other occupation given')),
    (25, _('(25) Criminal, suspect no other occupation given')),
    (26, _('(26) Unemployed no other occupation given')),
    (27, _('(27) Other only as last resort & explain')),
]

FUNCTION = [
    (0, _('(0) Do not know')),
    (1, _('(1) Subject')),
    (2, _('(2) Spokesperson')),
    (3, _('(3) Expert or commentator')),
    (4, _('(4) Personal Experience')),
    (5, _('(5) Eye Witness')),
    (6, _('(6) Popular Opinion')),
    (7, _('(7) Other')),
]

VICTIM_OF = [
    (0, _('(0) Not applicable (the story identifies the person only as a survivor)')),
    (1, _('(1) Victim of an accident, natural disaster, poverty')),
    (2, _('(2) Victim of domestic violence, rape, murder, etc.')),
    (3, _('(3) Victim of non-domestic sexual violence, rape, assault, etc (sexual violence only)')),
    (4, _('(4) Victim of other non-domestic crime, robbery, etc.')),
    (5, _('(5) Victim of violation based on religion, tradition...')),
    (6, _('(6) Victim of war, terrorism, vigilantism, state violence...')),
    (7, _('(7) Victim of discrimination based on gender, race, ethnicity, age, religion, ability, etc')),
    (8, _('(8) Other victim (specify in comments)')),
    (9, _('(9) Do not know, cannot decide')),
]

SURVIVOR_OF = [
    (0, _('(0) Not applicable (the story identifies the person only as a victim)')),
    (1, _('(1) Survivor of an accident, natural disaster, poverty')),
    (2, _('(2) Survivor of domestic violence, rape, murder, etc.')),
    (3, _('(3) Survivor of non-domestic sexual violence, rape, assault, etc. (sexual violence only)')),
    (4, _('(4) Survivor of other non-domestic crime, robbery, etc.')),
    (5, _('(5) Survivor of violation based on religion, tradition...')),
    (6, _('(6) Survivor of war, terrorism, vigilantism, state violence...')),
    (7, _('(7) Survivor of discrimination based on gender, race, ethnicity, age, religion, ability, etc.')),
    (8, _('(8) Other survivor (specify in comments)')),
    (9, _('(9) Do not know, cannot decide')),
]

IS_PHOTOGRAPH = [
    (1, _('(1) Yes')),
    (2, _('(2) No')),
    (3, _('(3) Do not know')),
]

AGREE_DISAGREE = [
    (1, _('(1) Agree')),
    (2, _('(2) Disagree')),
    (3, _('(3) Neither agree nor disagree')),
    (4, _('(4) Do not know')),
]

RETWEET = [
    (1, _('(1) Tweet')),
    (2, _('(2) Retweet')),
]

SPACE = [
    (1, _('(1) Full page')),
    (2, _('(2) Half page')),
    (3, _('(3) One third page')),
    (4, _('(4) Quarter page')),
    (5, _('(5) Less than quarter page')),
]

TV_ROLE = [
    (1, _('(1) Anchor, announcer or presenter: Usually in the television studio')),
    (2, _('(2) Reporter: Usually outside the studio. Include reporters who do not appear on screen, but whose voice is heard (e.g. as voice-over).')),
    (3, _('(3) Other journalist: Sportscaster, weather forecaster, commentator/analyst etc.')),
]

# The position of announcers and reporters in TV_ROLE
TV_ROLE_ANNOUNCER = TV_ROLE[0]
TV_ROLE_REPORTER = TV_ROLE[1]

# The id of reporters in TV_ROLE's
REPORTERS = 2

MEDIA_TYPES = [
    (1, 'Print'),
    (2, 'Radio'),
    (3, 'Television'),
    (4, 'Internet'),
    (5, 'Twitter')
]

TM_MEDIA_TYPES = [
    (1, 'Print'),
    (2, 'Radio'),
    (3, 'Television')
]

DM_MEDIA_TYPES = [
    (1, 'Internet'),
    (2, 'Twitter')
]

class CountryRegion(models.Model):
    """
    Model for mapping countries to regions

    """
    country = models.CharField(max_length=2, unique=True)
    region = models.CharField(max_length=30)


class SheetModel(models.Model):
    monitor = models.ForeignKey(Monitor, null=True)
    country = CountryField(null=True)
    country_region = models.ForeignKey(CountryRegion, null=True)


    class Meta:
        abstract = True

    @classmethod
    def person_field(self):
        """ Return the person-related field for this model
        """
        for fld in self._meta.get_all_related_objects():
            if fld.model and issubclass(fld.model, Person):
                return fld

    @classmethod
    def person_field_name(self):
        """ Return the nawe of the person-related field for this model
        """
        return self.person_field().name.split(':')[-1]

    @classmethod
    def journalist_field(self):
        """ Return the journalist-related field for this model
        """
        for fld in self._meta.get_all_related_objects():
            if fld.model and issubclass(fld.model, Journalist):
                return fld

    @classmethod
    def journalist_field_name(self):
        """ Return the nawe of the journalist-related field for this model
        """
        return self.journalist_field().name.split(':')[-1]


class Person(models.Model):
    class Meta:
        verbose_name = _('Person')
        abstract = True

    @classmethod
    def sheet_db_table(cls):
        return cls.sheet_field().foreign_related_fields[0].model._meta.db_table

    @classmethod
    def sheet_field(self):
        """ Return the sheet-related field for this model
        """
        for fld in self._meta.fields:
            if hasattr(fld, 'related') and fld.model and issubclass(fld.related.parent_model, SheetModel):
                return fld

    @classmethod
    def sheet_name(self):
        """ Return the name of the sheet relation field
        """
        for fld in self._meta.fields:
            if hasattr(fld, 'related') and fld.related and issubclass(fld.related.parent_model, SheetModel):
                return fld.name.split(':')[-1]


class Journalist(models.Model):
    # Journalists / Reporters
    sex = models.PositiveIntegerField(choices=GENDER, verbose_name=_('Journalist''s Sex'))
    age = models.PositiveIntegerField(choices=AGES, verbose_name=_('Age (person appears)'), null=True)
    tbl = dict(GENDER)

    def __unicode__(self):
        return u"%s" % (self.tbl[self.sex])

    class Meta:
        abstract = True

    @classmethod
    def sheet_db_table(cls):
        return cls.sheet_field().foreign_related_fields[0].model._meta.db_table

    @classmethod
    def sheet_field(self):
        """ Return the name of the sheet relation field
        """
        for fld in self._meta.fields:
            if hasattr(fld, 'related') and fld.related and issubclass(fld.related.parent_model, SheetModel):
                return fld

    @classmethod
    def sheet_name(self):
        """ Return the name of the sheet relation field
        """
        for fld in self._meta.fields:
            if hasattr(fld, 'related') and fld.related and issubclass(fld.related.parent_model, SheetModel):
                return fld.name.split(':')[-1]

class BroadcastJournalist(Journalist):
    role = models.PositiveIntegerField(choices=TV_ROLE, verbose_name=_('Role'))

    class Meta:
        abstract = True

##### Standard Fields ###########
field_scope = lambda x: models.PositiveIntegerField(choices=SCOPE, verbose_name=_('(%s) Scope' % x), help_text=_('Code the widest geographical scope that applies: if the event has both local and national importance, code national.'))
field_topic = lambda x: models.PositiveIntegerField(choices=TOPICS, verbose_name=_('(%s) Topic' % x), help_text=_('''Choose one topic that best describes how the story is reported. Remember that a single event can be reported in different ways. Within each broad category, we include a code for 'other stories'. Please use these codes only as a <strong>last resort</strong>.'''))

field_person_secondary = lambda x: models.PositiveIntegerField(choices=SOURCE, verbose_name=_('(%s) Source' % x), help_text=_('''<br><br>
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

# TODO - I am not sure whether all this force_text stuff will bypass translation or not. Without it, labels are shown containing __proxy__ objects
field_equality_rights = lambda x: models.CharField(choices=YESNO, verbose_name=_('(%s) Reference to gender equality / human rights legislation/ policy' % x), max_length=1, help_text=_('''Scan the full news story and code 'Yes' if it quotes or makes reference to any piece of legislation or policy that promotes gender equality or human rights.'''))
field_comments = lambda x: models.TextField(verbose_name=_('(%s) Describe any photographs included in the story and the conclusions you draw from them.' % x), blank=True)
field_about_women = lambda x, y: models.CharField(max_length=1, choices=YESNO, verbose_name=_('(%(field_number)s) Is the %(news_type)s about a particular woman or group of women?' % {"field_number" : x, "news_type" : force_text(y)}))
field_inequality_women = lambda x, y: models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=_('(%(field_number)s) This %(news_type)s clearly highlights issues of inequality between women and men' % {"field_number" : x, "news_type" : force_text(y)}))
field_stereotypes = lambda x, y: models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=_('(%s) Challenges Stereotypes') % x, help_text=_('This %s clearly challenges gender stereotypes' % force_text(y)))
field_further_analysis = lambda x, y: models.CharField(max_length=1, choices=YESNO, verbose_name=_('(%(field_number)s) Does this %(news_type)s warrant further analysis?' % {"field_number" : x, "news_type" : force_text(y)}), help_text=_('''<br><br>A %(news_type)s warrants further analysis if it clearly perpetuates or clearly challenges gender stereotypes, if it includes women's opinions in a remarkable way, if it contributes to an understanding of inequalities between women and men, if it mentions or calls attention to women's human rights, etc. Consult the guide for further explanation''' % {"news_type" : force_text(y)}))
field_url_and_multimedia = lambda x, y: models.TextField(verbose_name=_('(%(field_number)s) Copy and paste the URL of the %(news_type)s. Describe any photographs, images, other multimedia features included in the %(news_type)s. Note down the conclusions you draw from the images, audio and video.' % {"field_number" : x, "news_type" : force_text(y)}), blank=True)

field_num_female_anchors = models.PositiveIntegerField(verbose_name=_('Number of female anchors'), help_text=_('The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other'))

field_num_male_anchors = models.PositiveIntegerField(verbose_name=_('Number of male anchors'), help_text=_('The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other journalists</strong>'))
field_item_number = lambda x: models.PositiveIntegerField(verbose_name=_('(%s) Item Number' % x), help_text=_('Write in the number that describes the position of the story within the newscast. E.g. the first story in the newscast is item 1; the seventh story is item 7.'))
field_sex = lambda x: models.PositiveIntegerField(choices=GENDER, verbose_name=_('(%s) Sex' % x))

field_age = lambda x: models.PositiveIntegerField(choices=AGES, verbose_name=_('(%s) Age (person appears)' % x))
field_occupation = lambda x: models.PositiveIntegerField(choices=OCCUPATION, verbose_name=_('(%s) Occupation or Position' % x))
field_occupation_other = models.TextField(verbose_name=_('Other Occupation'), blank=True)
field_function = lambda x: models.PositiveIntegerField(choices=FUNCTION, verbose_name=_('(%s) Function in the news story' % x))
field_family_role = lambda x: models.CharField(max_length=1, choices=YESNO, verbose_name=_('(%s) Family Role Given?' % x), help_text=_('''Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.'''))
field_victim_or_survivor = lambda x: models.CharField(max_length=1, choices=YESNO,
    verbose_name=_('(%s) Does the story identify the person as either a victim or survivor?' % x),
    help_text=_('''<p>You should code a person as a <strong>victim</strong> either if the word 'victim' is used to describe her/him, or if the story Implies that the person is a victim - e.g. by using language or images that evoke particular emotions such as shock, horror, pity for the person.</p><p>You should code a person as a <strong>survivor</strong> either if the word 'survivor' is used to describe her/him, or if the story implies that the person is a survivor - e.g. by using language or images that evoke particular emotions such as admiration or respect for the person.</p>''')
    )
field_victim_of = lambda x: models.PositiveIntegerField(choices=VICTIM_OF, verbose_name=_('(%s) The story identifies the person as a victim of:' % x), null=True, blank=True)
field_victim_comments = lambda x: models.TextField(verbose_name=_('(%s) Add comments if ''Other Victim'' was selected above' % x), blank=True)
field_survivor_of = lambda x: models.PositiveIntegerField(choices=SURVIVOR_OF, verbose_name=_('(%s) The story identifies the person as a survivor of:' % x), null=True, blank=True)
field_survivor_comments = lambda x: models.TextField(verbose_name=_('(%s) Add comments if ''Other Survivor'' was selected above' % x), blank=True)
field_is_quoted = lambda x: models.CharField(max_length=1, choices=YESNO, verbose_name=_('(%s) Is the person directly quoted' % x),
    help_text=_('<p>A person is <strong>directly quoted</strong> if their own words are printed, e.g. "The war against terror is our first priority" said President Bush.</p><p>If the story paraphrases what the person said, that is not a direct quote, e.g. President Bush said that top priority would be given to fighting the war against terror.</p>')
)
field_is_photograph = lambda x: models.PositiveIntegerField(choices=IS_PHOTOGRAPH, verbose_name=_('(%s) Is there a photograph of the person in the story?' % x))
