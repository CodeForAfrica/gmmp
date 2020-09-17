from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from gmmp.models import Monitor


TOPICS = (
    (_('Politics and Government'), (
            (1,  _('(1) Women politicians, women electoral candidates...')),
            (2,  _('(2) Peace, negotiations, treaties...(local, regional, national),')),
            (3,  _('(3) Other domestic politics/government (local, regional, national), elections, speeches, the political process ...')),
            (4,  _('(4) Global partnerships (international trade and finance systems, e.g. WTO, IMF, World Bank, debt) ...')),
            (5,  _('(5) Foreign/international politics, relations with other countries, negotiations, treaties, UN peacekeeping ...')),
            (6,  _('(6) National defence, military spending, military training, military parades, internal security ...')),
            (7,  _('(7) Other stories on politics and government (specify the topic in \'Comments\' section of coding sheet)')),
        )
    ),
    (_('Economy'), (
            (8,  _('(8) Economic policies, strategies, modules, indicators, stock markets, taxes,...')),
            (9,  _('(9) Economic crisis, state bailouts of companies, company takeovers and mergers ...')),
            (10, _('(10) Poverty, housing, social welfare, aid to those in need ...')),
            (11, _('(11) Women’s participation in economic processes (informal work, paid employment, unemployment, unpaid labour)')),
            (12, _('(12) Employment')),
            (13, _('(13) Informal work, street vending, ...')),
            (14, _('(14) Other labour issues, strikes, trade unions, negotiations, other employment and unemployment')),
            (15, _('(15) Rural economy, agriculture, farming practices, agricultural policy, land rights ...')),
            (16, _('(16) Consumer issues, consumer protection, regulation, prices, consumer fraud ...')),
            (17, _('(17) Transport, traffic, roads...')),
            (18, _('(18) Other stories on the economy (specify the topic in \'Comments\' section of coding sheet)')),
        )
    ),
    (_('Science and Health'), (
            (19, _('(19) Science, technology, research, funding, discoveries, developments ...')),
            (20, _('(20) Medicine, health, hygiene, safety, disability, medical research, funding (not EBOLA or HIV- AIDS)...')),
            (21, _('(21) EBOLA, treatment, response...')),
            (22, _('(22) HIV and AIDS, incidence, policy, treatment, people affected ...')),
            (23, _('(23) Other epidemics, viruses, contagions, Influenza, BSE, SARS. NOT COVID-19 (For stories related to Covid-19 choose the closest relevant sub-topic)')),
            (24, _('(24) Birth control, fertility, sterilization, amniocentesis, termination of pregnancy ...')),
            (25, _('(25) Climate change, global warming')),
            (26, _('(26) Environment, pollution, tourism ...')),
            (27, _('(27) Other stories on science or health (specify the topic in \'Comments\' section of coding sheet)')),
        )
    ),
    (_('Social and Legal'), (
            (28, _('(28) Sustainable Development Goals (SDGs), Post 2015 agenda, Agenda 2030')),
            (29, _('(29) Family relations, inter-generational conflict, single parents ...')),
            (30, _('(30) Human rights, women\'s rights, children\'s rights, gay & lesbian rights, rights of minorities ..')),
            (31, _('(31) Religion, culture, tradition, cultural controversies, teachings, celebrations, practices ...')),
            (32, _('(32) Migration, refugees, asylum seekers, ethnic conflict, integration, racism, xenophobia ...')),
            (33, _('(33) Other development issues, sustainability,')),
            (34, _('(34) Education, childcare, nursery, university, literacy')),
            (35, _('(35) Women\'s movement, feminist activism, events, demonstrations, gender equality advocacy ...')),
            (36, _('(36) Changing gender relations, roles and relationships of women and men inside and outside the home ...')),
            (37, _('(37) Family law, family codes, property law, inheritance law and rights ...')),
            (38, _('(38) Legal system, judicial system, legislation (apart from family, property & inheritance law) ...')),
            (39, _('(39) Disaster, accident, famine, flood, plane crash, etc')),
            (40, _('(40) Riots, demonstrations, public disorder, etc.')),
            (41, _('(41) Other stories on social or legal issues (specify the topic in \'Comments\' section of coding sheet)')),
        )
    ),
    (_('Crime and Violence'), (
            (42, _('(42) Non-violent crime, bribery, theft, drug-dealing, ...')),
            (43, _('(43) Corruption, (including political corruption/malpractice)')),
            (44, _('(44) Violent crime, murder, abduction, kidnapping, assault, drug-related violence ...')),
            (45, _('(45) Child abuse, sexual violence against children, neglect')),
            (46, _('(46) War, civil war, terrorism, state-based violence')),
            (47, _('(47) Other stories on crime and violence (specify the topic in \'Comments\' section of coding sheet)')),
        )
    ),
    (_('Gender and related'), (
            (48, _(u'(48) Sexual harassment against women, rape, sexual assault, #MeToo #TimesUp')),
            (49, _('(49) Other gender violence such as feminicide, trafficking of girls and women, FGM...')),
            (50, _('(50) Inequality between women and men such as income inequality/gender pay gap,')),
        )
    ),
    (_('Celebrity, Arts and Media, Sports'), (
            (51, _('(51) Celebrity news, births, marriages, deaths, obituaries, famous people, royalty ...')),
            (52, _('(52) Arts, entertainment, leisure, cinema, theatre, books, dance ...')),
            (53, _('(53) Media, including new media (computers, internet), portrayal of women and/or men')),
            (54, _('(54) Fake news, mis-information, dis-information, mal-information...')),
            (55, _('(55) Beauty contests, models, fashion, beauty aids, cosmetic surgery ...')),
            (56, _('(56) Sports, events, players, facilities, training, policies, funding ...')),
            (57, _('(57) Other stories on celebrities, arts, media (specify the topic in \'Comments\' section of coding sheet)')),
        )
    ),
    (_('Other'), (
            (58, _('(58) Use only as a last resort and explain')),
        )
    )
)

SCOPE = (
    (1, _('(1) Local')),
    (2, _('(2) National')),
    (3, _('(3) Sub-Regional and Regional')),
    (4, _('(4) Foreign/International')),
)

YESNO = (
    ('Y', _('(1) Yes')),
    ('N', _('(2) No')),
)

MONITOR_MODE = (
    (1, _('Full monitoring')),
    (2, _('Short monitoring')),
)

YESNO_NUMBER = (
    (1, _('(1) Yes')),
    (2, _('(2) No')),
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

AGES_PEOPLE_IN_THE_NEWS = (
    (0, _('(0) Do not know')),
    (1, _('(1) 12 and under')),
    (2, _('(2) 13-18')),
    (3, _('(3) 19-34')),
    (4, _('(4) 35-49')),
    (5, _('(5) 50-64')),
    (6, _('(6) 65-79')),
    (7, _('(7) 80 years or more')),
)

SOURCE = (
    (0, _('(0) Do not know')),
    (1, _('(1) Person')),
    (2, _('(2) Secondary Source')),
)

OCCUPATION = [
    (0,  _('(0) Not stated')),
    (1,  _('(1) Royalty, monarch, deposed monarch, etc.')),
    (2,  _('(2) Politician/ member of parliament, ...')),
    (3,  _('(3) Government employee, public servant, spokesperson, etc.')),
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

# The id of reporters in TV_ROLE
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
    monitor = models.ForeignKey(Monitor, null=True, on_delete=models.SET_NULL)
    monitor_mode = models.IntegerField(choices=MONITOR_MODE, default=1, verbose_name=_('Format'))
    country = CountryField(null=True)
    country_region = models.ForeignKey(CountryRegion, null=True, on_delete=models.SET_NULL)


    class Meta:
        abstract = True

    @classmethod
    def person_field(cls):
        """ Return the person-related field for this model
        """
        for fld in cls._meta.get_all_related_objects():
            if fld.model and issubclass(fld.model, Person):
                return fld

    @classmethod
    def person_field_name(cls):
        """ Return the name of the person-related field for this model
        """
        return cls.person_field().name.split(':')[-1]

    @classmethod
    def journalist_field(cls):
        """ Return the journalist-related field for this model
        """
        for fld in cls._meta.get_all_related_objects():
            if fld.model and issubclass(fld.model, Journalist):
                return fld

    @classmethod
    def journalist_field_name(cls):
        """ Return the name of the journalist-related field for this model
        """
        return cls.journalist_field().name.split(':')[-1]


class Person(models.Model):
    class Meta:
        verbose_name = _('Person')
        abstract = True

    @classmethod
    def sheet_db_table(cls):
        return cls.sheet_field().foreign_related_fields[0].model._meta.db_table

    @classmethod
    def sheet_field(cls):
        """ Return the sheet-related field for this model
        """
        for fld in cls._meta.fields:
            if hasattr(fld, 'related') and fld.model and issubclass(fld.related.parent_model, SheetModel):
                return fld

    @classmethod
    def sheet_name(cls):
        """ Return the name of the sheet relation field
        """
        for fld in cls._meta.fields:
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
    def sheet_field(cls):
        """ Return the name of the sheet relation field
        """
        for fld in cls._meta.fields:
            if hasattr(fld, 'related') and fld.related and issubclass(fld.related.parent_model, SheetModel):
                return fld

    @classmethod
    def sheet_name(cls):
        """ Return the name of the sheet relation field
        """
        for fld in cls._meta.fields:
            if hasattr(fld, 'related') and fld.related and issubclass(fld.related.parent_model, SheetModel):
                return fld.name.split(':')[-1]

class BroadcastJournalist(Journalist):
    role = models.PositiveIntegerField(choices=TV_ROLE, verbose_name=_('Role'))

    class Meta:
        abstract = True

##### Standard Fields ###########
field_scope = lambda x: models.PositiveIntegerField(choices=SCOPE, verbose_name=x, help_text=_('Code the widest geographical scope that applies: if the event has both local and national importance, code national.'))
field_covid19 = lambda x: models.PositiveIntegerField(choices=YESNO_NUMBER, verbose_name=x, help_text=_('''Note: For the question below it is important <strong>NOT</strong> to code COVID19-related stories under topic 23 but to choose the most relevant <strong>secondary</strong> topic theme in order to ensure results that can be compared with those from previous GMMPs.'''))
field_topic = lambda x: models.PositiveIntegerField(choices=TOPICS, verbose_name=x, help_text=_('''If the story <strong>IS</strong> COVID19-related (indicated by answer choice (1) in question (z) above, choose the <strong>topic</strong> category which is the most relevant as the <strong>secondary</strong> topic theme, <strong>NOT</strong> topic 23. For example, if the story is about job losses due to COVID-19, it should be coded under topic 12 <em>‘Employment’</em>; or if the story is about the spread of COVID-19 in a refugee camp, it should be coded under topic 32 <em>‘Migration, refugees...’</em>. '''))

field_equality_rights = lambda x: models.CharField(choices=YESNO, verbose_name=x, max_length=1, help_text=_('''Scan the full news story and code 'Yes' if it quotes or makes reference to any piece of legislation or policy that promotes gender equality or human rights.'''))
field_about_women = lambda x: models.CharField(max_length=1, choices=YESNO, verbose_name=x)
field_inequality_women = lambda x: models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=x)
field_stereotypes = lambda x: models.PositiveIntegerField(choices=AGREE_DISAGREE, verbose_name=x)

field_comments = lambda x: models.TextField(verbose_name=x, blank=True)

field_further_analysis = lambda x, y: models.CharField(max_length=1, choices=YESNO, verbose_name=x, help_text=y)
field_url_and_multimedia = lambda x: models.TextField(verbose_name=x, blank=True)

field_num_anchors = lambda x: models.PositiveIntegerField(verbose_name=x, help_text=_('The anchor (or announcer, or presenter) is the person who introduces the newscast and the individual items within it. <strong>Note: You should only include the anchors/announcers. Do not include reporters or other journalists</strong>'))

field_item_number = lambda x: models.PositiveIntegerField(verbose_name=x, help_text=_('Write in the number that describes the position of the story within the newscast. E.g. the first story in the newscast is item 1; the seventh story is item 7.'), blank=True, null=True)

field_sex = lambda x: models.PositiveIntegerField(choices=GENDER, verbose_name=x, null=True, blank=True)

field_age = lambda x: models.PositiveIntegerField(choices=AGES_PEOPLE_IN_THE_NEWS, verbose_name=x, null=True, blank=True)
field_occupation = lambda x: models.PositiveIntegerField(choices=OCCUPATION, verbose_name=x, null=True, blank=True)
field_occupation_other = models.TextField(verbose_name=_('Other Occupation'), blank=True)
field_function = lambda x: models.PositiveIntegerField(choices=FUNCTION, verbose_name=x, null=True, blank=True)
field_family_role = lambda x: models.CharField(max_length=1, choices=YESNO, verbose_name=x, help_text=_('''Code yes only if the word 'wife', 'husband' etc is actually used to describe the person.'''), blank=True, null=True)
field_victim_or_survivor = lambda x: models.CharField(max_length=1, choices=YESNO,
    verbose_name=x,
    blank=True,
    null=True,
    help_text=_('''You should code a person as a victim <strong>either</strong> if the word 'victim' is used to describe her/him, <strong>or</strong> if the story Implies that the person is a victim - e.g. by using language or images that evoke particular emotions such as shock, horror, pity for the person.<br/>You should code a person as a survivor <strong>either</strong> if the word 'survivor' is used to describe her/him, <strong>or</strong> if the story implies that the person is a survivor - e.g. by using language or images that evoke particular emotions such as admiration or respect for the person.'''))
field_victim_of = lambda x: models.PositiveIntegerField(choices=VICTIM_OF, verbose_name=x, null=True, blank=True)
field_victim_comments = lambda x: models.TextField(verbose_name=_('(%s) Add comments if ''Other Victim'' was selected above' % x), blank=True)
field_survivor_of = lambda x: models.PositiveIntegerField(choices=SURVIVOR_OF, verbose_name=x, null=True, blank=True)
field_survivor_comments = lambda x: models.TextField(verbose_name=_('(%s) Add comments if ''Other Survivor'' was selected above' % x), blank=True)
field_is_quoted = lambda x: models.CharField(max_length=1, choices=YESNO, verbose_name=x,
    blank=True,
    null=True,
    help_text=_('A person is <strong>directly quoted</strong> if their own words are printed, e.g. "The war against terror is our first priority" said President Bush.<br/>If the story paraphrases what the person said, that is not a direct quote, e.g. President Bush said that top priority would be given to fighting the war against terror.')
)
field_is_photograph = lambda x: models.PositiveIntegerField(choices=IS_PHOTOGRAPH, verbose_name=x, blank=True, null=True)

field_special_qn = lambda x: models.CharField(choices=YESNO, max_length=1, blank=True, verbose_name=x)
