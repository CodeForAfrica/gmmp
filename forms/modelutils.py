from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class SheetModel(models.Model):
    monitor = models.ForeignKey(User, null=False)

    class Meta:
        abstract = True

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

