import openpyxl
import json
import os
import logging
import re

from reports.report_details import WS_INFO


RECODES = {
    'Pacific': 'Pacific Islands',
    'Congo, Rep (Brazzaville)': 'Congo',
    'Congo, Dem Rep': 'Congo (the Democratic Republic of the)',
    'Bosnia & Herzegovina': 'Bosnia and Herzegovina',
    'St Lucia': 'Saint Lucia',
    'St. Vincent and The Grenadines': 'Saint Vincent and the Grenadines',
    'Trinidad & Tobago': 'Trinidad and Tobago',
    'Female  %F': 'Female',
    # women topics
    "Arts, entertainment, leisure, cinema, theatre, books, dance": "Arts, entertainment, leisure, cinema, books, dance",
    "Beauty contests, models, fashion, beauty aids, cosmetic surgery": "Beauty contests, models, fashion, cosmetic surgery",
    "Birth control, fertility, sterilisation, amniocentesis, termination of pregnancy": "Birth control, fertility, sterilization, termination...",
    "Celebrity news, births, marriages, deaths, obituaries, famous people, royalty": "Celebrity news, births, marriages, royalty, etc.",
    "Changing gender relations, roles and relationships of women and men inside and outside the home": "Changing gender relations (outside the home)",
    "Child abuse, sexual violence against children, trafficking, neglect.": "Child abuse, sexual violence against children, neglect",
    "Consumer issues, consumer protection, regulation, prices, consumer fraud": "Consumer issues, consumer protection, fraud...",
    "Development issues, sustainability, community development": "Other development issues, sustainability, etc.",
    "Disaster, accident, famine, earthquake, flood, hurricane, plane crash, car crash": "Disaster, accident, famine, flood, plane crash, etc.",
    "Economic crisis, state bailouts of companies, company takeovers and mergers": "Economic crisis, state bailouts of companies, company takeovers and mergers, etc.",
    "Education, child care, nurseries, pre-school to university, adult education, literacy": "Education, childcare, nursery, university, literacy",
    "Environment, nature,   pollution, global warming, ecology, tourism": "Environment, pollution, tourism",
    "Family law, family codes, property law, inheritance law and rights": "Family law, family codes, property law, inheritance...",
    "Family relations, inter-generational conflict, single parents": "Family relations, inter-generational conflict, parents",
    "Foreign/international politics, relations with other countries, negotiations, treaties, UN peacekeeping": "Foreign/international politics, UN, peacekeeping",
    "Gender-based violence, feminicide, harassment, domestic violence, rape, trafficking, genital mutilation": "Gender violence based on culture, family, inter-personal relations, feminicide, harassment, rape, sexual assault, trafficking, FGM...",
    "HIV and AIDS, incidence, policy, treatment, people affected": "HIV and AIDS, policy, treatment, etc",
    "Human rights, women's rights, children's rights, gay & lesbian rights, rights of minorities ..": "Human rights, womens rights, rights of sexual minorities, rights of religious minorities, etc.",
    "Legal system, judicial system, legislation (apart from family, property & inheritance law)": "Legal system, judiciary, legislation apart from family",
    "Media, including new media (computers, internet), portrayal of women and/or men, pornography": "Media, (including internet), portrayal of women/men",
    "Medicine, health, hygiene, safety, disability, medical research, funding (apart from HIV-AIDS)": "Medicine, health, hygiene, safety, (not EBOLA or HIV/AIDS)",
    "Migration, refugees, asylum seekers, ethnic conflict, integration, racism, xenophobia": "Migration, refugees, xenophobia, ethnic conflict...",
    "National defence, military spending, military training, military parades, internal security": "National defence, military spending, internal security, etc.",
    "Non-violent crime, bribery, theft, drug-dealing, corruption, (including political corruption/malpractice)": "Non-violent crime, bribery, theft, drugs, corruption",
    "Other epidemics, viruses, contagions, Influenza, BSE, SARS": "Other epidemics, viruses, contagions, Influenza, BSE, SARS",
    "Other labour issues, strikes, trade unions, negotiations, other employment and unemployment": "Other labour issues (strikes, trade unions, etc.)",
    "Other stories on celebrities, arts, media (specify the subject in 'Comments' section of coding sheet)": "Other stories on politics (specify in comments)",
    "Other stories on crime and violence (specify the subject in 'Comments' section of coding sheet)": "Other stories on science (specify in comments)",
    "Other stories on politics and government (specify the subject in 'Comments' section of coding sheet)": "Other stories on politics (specify in comments)",
    "Other stories on science or health (specify the subject in 'Comments' section of coding sheet)": "Other stories on science (specify in comments)",
    "Other stories on social or legal issues (specify the subject in 'Comments' section of coding sheet)": "Other stories on social/legal (specify in comments)",
    "Other stories on the economy (specify the subject in 'Comments' section of coding sheet)": "Other stories on economy (specify in comments)",
    "Peace, negotiations, treaties(local, regional, national),": "Peace, negotiations, treaties",
    "Poverty, housing, social welfare, aid to those in need": "Poverty, housing, social welfare, aid, etc.",
    "Religion, culture, tradition, controversies, teachings, celebrations, practices": "Religion, culture, tradition, controversies...",
    "Riots, demonstrations, public disorder": "Riots, demonstrations, public disorder, etc.",
    "Rural economy, agriculture, farming practices, agricultural policy, land rights": "Rural economy, agriculture, farming, land rights",
    "Science, technology, research, funding, discoveries, developments": "Science, technology, research, discoveries...",
    "Sports, events, players, facilities, training, policies, funding": "Sports, events, players, facilities, training, funding",
    "Transport, traffic, roads": "Transport, traffic, roads...",
    "Violent crime, murder, abduction, kidnapping, assault, drug-related violence": "Violent crime, murder, abduction, assault, etc.",
    "War, civil war, terrorism, state-based violence": "War, civil war, terrorism, other state-based violence",
    "Women's movement, activism, events, demonstrations, gender equality advocacy": "Womens movement, activism, demonstrations, etc",
    "Other domestic politics/government (local, regional, national), elections, speeches, the political process": "Other domestic politics, government, etc.",
    "Global partnerships (international trade and finance systems, e.g. WTO, IMF, World Bank, debt)": "Global partnerships",
    # occupations
    "Agriculture, mining, fishing, forestry worker": "Agriculture, mining, fishing, forestry",
    "Celebrity, artist, actor, writer, singer, radio or television personality": "Celebrity, artist, actor, writer, singer, TV personality",
    "Government employee, public servant, bureaucrat, diplomat, intelligence officer": "Government employee, public servant, etc.",
    "Homemaker, parent, either female or male. Code this only if no other occupation is given, e.g. a doctor who is also described as a mother is coded 6.": "Homemaker, parent (male or female)) only if no other occupation is given e.g. doctor/mother=code 6",
    "Lawyer, judge, magistrate, legal advocate, legal expert, legal clerk": "Lawyer, judge, magistrate, legal advocate, etc.",
    "Media professional, journalist, video or film-maker, theatre director ...": "Media professional, journalist, film-maker, etc.",
    "Office or service worker, non-management worker in office, store, restaurant, catering": "Office or service worker, non-management worker",
    "Police, military, para-military group, militia, prison officer, security officer, fire officer": "Police, military, para-military, militia, fire officer",
    "Religious figure, priest, monk, rabbi, mullah, nun": "Religious figure, priest, monk, rabbi, mullah, nun",
    "Royalty, ruling monarch, deposed monarch, any member of royal family": "Royalty, monarch, deposed monarch, etc.",
    "Science or technology professional, engineer, technician, computer specialist": "Science/ technology professional, engineer, etc.",
    "Sportsperson, athlete, player, coach, referee": "Sportsperson, athlete, player, coach, referee",
    "Student, pupil, schoolchild": "Student, pupil, schoolchild",
    "Tradesperson, artisan, labourer, truck driver, construction, factory, domestic worker": "Tradesperson, artisan, labourer, truck driver, etc.",
    "Government official, politician, president, government minister, political leader, political party staff, spokesperson": "Government, politician, minister, spokesperson...",
    "Business person, executive, manager, entrepreneur, economist, financial expert, stock broker": "Business person, exec, manager, stock broker...",
    "Child, young person (up to 18 years). Code this only if no other occupation/position is given, e.g. a schoolchild is coded 19; a child labourer is coded 12.": "Child, young person no other occupation given",
    "Villager or resident engaged in unspecified occupation. Code this only if no other occupation is given, e.g. a teacher who is also described as a villager is coded 5.": "Villager or resident no other occupation given",
    "Criminal, suspect. Code this only if no other occupation is given, e.g, a lawyer suspected of committing a crime is coded 9; a former politician who has committed a crime is coded 2.": "Criminal, suspect no other occupation given",
    "Unemployed. Code this only if no other occupation is given, e.g. an unemployed actor is coded 17; an unemployed person who commits a crime is coded 24.": "Unemployed no other occupation given",
    "Sex worker, prostitute": "Sex worker",
    "Other. Use only as a last resort (specify the occupation/position in 'Comments' section of coding sheet)": "Other only as last resort & explain",
    "Retired person, pensioner. Code this only if no other occupation is given, e.g. a retired police officer is coded 4; a retired politician is coded 2.": "Retired person, pensioner no other occupation given",
    "Activist or worker in civil society organisation, non-governmental organisation, trade union, human rights, consumer issues, environment, aid agency, peasant leader, United Nations": "Activist or worker in civil society org., NGO, trade union",
    "Subject: the story is about this person, or about something the person has done, said etc.": "Subject",
    "Spokesperson: the person represents, or speaks on behalf of another person, a group or an organisation": "Spokesperson",
    "Expert or commentator: the person provides additional information, opinion or comment, based on specialist knowledge or expertise": "Expert or commentator",
    "Personal experience: the person provides opinion or comment, based on individual personal experience; the opinion is not necessarily meant to reflect the views of a wider group": "Personal Experience",
    "Eye witness: the person gives testimony or comment, based on direct observation (e.g. being present at an event)": "Eye Witness",
    "Popular opinion: the person's opinion is assumed to reflect that of the 'ordinary citizen' (e.g., in a street interview, vox populi etc); it is implied that the person's point of view is shared by a wider group of people.": "Popular Opinion",
    "Other. Use only as a last resort (describe the function in 'Comments' section of coding sheet).": "Other",
    "12 years or under": "12 and under",
    "%F": "Female",
    "%M": "Male"
}


def canon(key):
    key = key.replace(u'\u2026', '')
    key = recode(key.strip())
    return key.strip().lower()


def recode(v):
    return RECODES.get(v, v)


def v(v):
    """
    Try to interpret a value as an percentage
    """
    if not isinstance(v, basestring):
        return v

    m = re.match(r'^(\d+(\.\d+)?)(%)?$', v)
    if m:
        if not m.group(2):
            # int
            v = int(m.group(1))
        else:
            # float
            v = float(m.group(1))

        if m.group(3):
            v = v / 100.0
    return v


class Historical(object):
    log = logging.getLogger(__name__)

    def __init__(self, historical_file='historical.json'):
        self.fname = historical_file
        self.load()

    def load(self):
        if os.path.exists(self.fname):
            with open(self.fname, 'r') as f:
                self.all_data = json.load(f)
        else:
            self.all_data = {}

    def save(self):
        with open(self.fname, 'w') as f:
            json.dump(self.all_data, f, indent=2, sort_keys=True)

    def get(self, new_ws, coverage):
        sheet = WS_INFO['ws_' + new_ws]

        if 'historical' not in sheet:
            raise KeyError('New worksheet %s is not linked to an historical worksheet' % new_ws)
        old_ws = sheet['historical']

        if old_ws not in self.all_data[coverage]:
            raise KeyError('Old worksheet %s does not have any historical data' % old_ws)

        return self.all_data[coverage][sheet['historical']]

    def import_from_file(self, fname, coverage):
        # TODO: regional? country? global?
        wb = openpyxl.load_workbook(fname, read_only=True, data_only=True)

        for old_sheet, new_sheet in self.historical_sheets():
            ws = wb[old_sheet]

            self.log.info("Importing sheet %s" % old_sheet)
            data = getattr(self, 'import_%s' % old_sheet)(ws, new_sheet)
            self.log.info("Imported sheet %s" % old_sheet)

            if coverage not in self.all_data:
                self.all_data[coverage] = {}

            self.all_data[coverage][old_sheet] = data

    def historical_sheets(self):
        return [(sheet['historical'], sheet) for sheet in WS_INFO.itervalues() if 'historical' in sheet]

    def import_1F(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(ws, data, col_start=15, col_end=18, row_end=12)

        return all_data

    def import_2F(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(ws, data, col_start=15, col_end=18, row_start=6, row_end=114)

        return all_data

    def import_3aF(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_table(ws, data, col_start=6, col_end=13, row_end=11, col_heading_row=3)

        return all_data

    def import_9aF(self, ws, sheet_info):
        all_data = {}
        self.slurp_year_grouped_table(ws, all_data, col_start=6, cols=1, cols_per_group=5, year_heading_row=4, col_heading_row=3, row_start=5, row_end=12)
        return all_data

    def import_9bF(self, ws, sheet_info):
        data = {}
        self.slurp_year_grouped_table(ws, data, col_start=6, cols=3, cols_per_group=5, year_heading_row=3, col_heading_row=2, row_start=4, row_end=5)
        return data

    def import_9cF(self, ws, sheet_info):
        data = {}
        self.slurp_year_grouped_table(ws, data, col_start=6, cols=1, cols_per_group=5, year_heading_row=3, col_heading_row=2, row_start=5, row_end=8)
        return data

    def import_9dF(self, ws, sheet_info):
        data = {}
        all_data = {2010: data}

        col_heading = canon('Female')
        col_data = {}
        data[col_heading] = col_data

        for irow in xrange(4, 55):
            row_heading = canon(ws.cell(column=5, row=irow).value)
            col_data[row_heading] = v(ws.cell(column=8, row=irow).value)

        return all_data

    def import_9eF(self, ws, sheet_info):
        data = {}
        self.slurp_year_grouped_table(ws, data, col_start=6, cols=1, cols_per_group=5, year_heading_row=3, col_heading_row=2, row_start=5, row_end=30)
        return data

    def import_9fF(self, ws, sheet_info):
        data = {}
        self.slurp_year_grouped_table(ws, data, col_start=6, cols=1, cols_per_group=5, year_heading_row=3, col_heading_row=2, row_start=5, row_end=12)
        return data

    def import_20aF(self, ws, sheet_info):
        data = {}
        self.slurp_year_grouped_table(ws, data, col_start=6, cols=1, cols_per_group=5, year_heading_row=3, col_heading_row=2, row_start=5, row_end=30)
        return data

    def import_20bF(self, ws, sheet_info):
        year = 2010
        data = {}
        all_data = {year: data}

        self.slurp_secondary_col_table(ws, data, col_start=42, cols=6, cols_per_group=2, major_col_heading_row=3, row_start=6, row_end=11)
        return all_data

    def slurp_secondary_col_table(self, ws, data, col_start, cols_per_group, cols, row_end, row_start=5, major_col_heading_row=4, row_heading_col=5):
        """
        Get values from a table with two levels of column headings.
        """
        for icol in xrange(col_start, col_start + cols * cols_per_group, cols_per_group):
            major_col_heading = canon(ws.cell(column=icol, row=major_col_heading_row).value)
            major_col_data = {}
            data[major_col_heading] = major_col_data

            for isec_col in xrange(icol, icol + cols_per_group):
                col_heading = canon(ws.cell(column=isec_col, row=major_col_heading_row + 1).value)
                col_data = {}
                major_col_data[col_heading] = col_data

                for irow in xrange(row_start, row_end + 1):
                    row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                    col_data[row_heading] = v(ws.cell(column=isec_col, row=irow).value)

    def slurp_table(self, ws, data, col_start, col_end, row_end, row_start=5, col_heading_row=4, row_heading_col=5):
        """
        Grab values from a simple table with column and row titles.
        """
        for icol in xrange(col_start, col_end + 1):
            col_heading = canon(ws.cell(column=icol, row=col_heading_row).value)
            col_data = {}
            data[col_heading] = col_data

            for irow in xrange(row_start, row_end):
                row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                col_data[row_heading] = v(ws.cell(column=icol, row=irow).value)

    def slurp_year_grouped_table(self, ws, all_data, col_start, cols_per_group, cols, row_end, row_start=5, year_heading_row=4, col_heading_row=3, row_heading_col=5):
        """
        Slurp a table where each category contains a range of years.

        eg.
             Category 1      | Category 2      |
             2005 | 2010 | N | 2005 | 2010 | N |
        row1
        row2
        row3
        """
        for icol in xrange(col_start, col_start + cols * cols_per_group, cols_per_group):
            col_heading = canon(ws.cell(column=icol, row=col_heading_row).value)

            for iyear in xrange(icol, icol + cols_per_group):
                year = ws.cell(column=iyear, row=year_heading_row).value
                if year in ['N', 'N-F']:
                    year = 2010
                    effective_col_heading = canon('N')
                else:
                    year = int(year)
                    effective_col_heading = col_heading

                if year not in all_data:
                    all_data[year] = {}

                data = all_data[year]
                col_data = {}
                data[effective_col_heading] = col_data

                for irow in xrange(row_start, row_end + 1):
                    row_heading = canon(ws.cell(column=row_heading_col, row=irow).value)
                    col_data[row_heading] = v(ws.cell(column=iyear, row=irow).value)
