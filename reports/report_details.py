from collections import OrderedDict

from django_countries import countries

from forms.models import sheet_models
from forms.modelutils import CountryRegion


def get_regions():
    """
    Return a (id, region_name) list for all regions
    """
    country_regions = CountryRegion.objects\
                        .values('region')\
                        .exclude(region='Unmapped')\
                        .exclude(region='Global')\
                        .exclude(region='Transnational')
    regions = set(item['region'] for item in country_regions)
    return [(i, region) for i, region in enumerate(sorted(list(regions)))]


def get_countries():
    """
    Return a (code, country) list for countries captured.
    """
    captured_country_codes = set()
    for model in sheet_models.values():
        rows = model.objects.values('country')
        captured_country_codes.update([r['country'] for r in rows])
    all_countries = [(code, name) for code, name in list(countries) if code in captured_country_codes]
    all_countries.append(('BE', 'Belgium - French and Flemish'))
    all_countries.append(('GB', 'United Kingdom - England, Northern Ireland, Scotland and Wales'))
    all_countries.sort(key=lambda p: p[1])
    return all_countries


def get_region_countries(region):
    """
    Return a (code, country) list for a region.
    """
    if region == 'ALL':
        return get_countries()
    else:
        country_codes = REGION_COUNTRY_MAP[region]
        return [(code, name) for code, name in list(countries) if code in country_codes]


def get_country_region(country):
    """
    Return a (id, region_name) list to which a country belongs.
    """
    if country == 'ALL':
        return get_regions()
    else:
        return [(0, [k for k, v in list(REGION_COUNTRY_MAP.items()) if country in v][0])]


def add_transnational_to_regions(regions):
    """
    Append Transnational to region list for use in sheets 79-98 if not included
    """
    all_regions = regions + [(len(regions), u'Transnational')]
    return all_regions


WS_INFO = {
    'ws_01': {
        '2015': {
            'name': '1',
            'historical': '1',
            'title': 'Participating Countries',
            'desc': 'Breakdown of all media by region',
            'reports': ['global'],
        },
        '2010': {
            'name': '1',
            'historical': '1F',
            'title': 'Participating Countries',
            'desc': 'Breakdown of all media by region',
            'reports': ['global'],
        },
    },
    'ws_02': {
        '2015': {
            'name': '2',
            'title': 'Participating Countries in each Region',
            'desc': 'Breakdown of all media by country',
            'reports': ['global', 'region'],
            'historical': '2',
        },
        '2010': {
            'name': '2',
            'title': 'Participating Countries in each Region',
            'desc': 'Breakdown of all media by country',
            'reports': ['global', 'region'],
            'historical': '2F',
        },
    },
    'ws_03': {
        '2015': {
            'name': '3',
            'title': 'Counts of media monitored',
            'desc': 'Total number of distinct media monitored',
            'reports': ['global'],
            'historical': '3'
        },
        '2010': {
            'name': '3',
            'title': 'Counts of media monitored',
            'desc': 'Total number of distinct media monitored',
            'reports': ['global'],
            'historical': '2aF'
        },
    },
    'ws_04': {
        '2015': {
            'name': '4',
            'title': 'Topics in the news by region',
            'desc': 'Breakdown of major news topics by region by medium',
            'reports': ['global', 'region', 'country'],
            'historical': '4',
        },
        '2010': {
            'name': '4',
            'title': 'Topics in the news by region',
            'desc': 'Breakdown of major news topics by region by medium',
            'reports': ['global', 'region'],
            'historical': '3aF'
        },
    },
    'ws_05': {
        '2015': {
            'name': '5',
            'historical': '5',
            'title': 'Overall presence of women in news',
            'desc': 'Summary of news subjects, by sex, by GMMP year',
            'reports': ['global', 'region', 'country'],
        },
        '2010': {
            'name': '5',
            'historical': '9aF',
            'title': 'Summary of women in the news, by GMMP year',
            'desc': 'Overall presence of women in news',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_06': {
        '2015': {
            'name': '6',
            'title': 'Women in the news (sources) in major news topics by region',
            'desc': 'Breakdown of women in the news in major topics by region',
            'reports': ['global', 'region', 'country'],
            'historical': '6',
        },
        '2010': {
            'name': '6',
            'title': 'Breakdown of women in the news in major topics by region',
            'desc': 'Women in the news (sources) in major news topics by region ',
            'reports': ['global', 'region'],
            'historical': '3bF',
        },
    },
    'ws_07': {
        '2015': {
            'name': '7',
            'title': 'Women in the news (sources) by medium',
            'desc': 'Breakdown by sex of all mediums',
            'reports': ['global', 'region', 'country'],
            'historical': '7',
        },
        '2010': {
            'name': '7',
            'title': 'Women in the news (sources) by medium',
            'desc': 'Breakdown by sex of all mediums',
            'reports': ['global', 'region', 'country'],
            'historical': '9bF',
        },
    },
    'ws_08': {
        '2015': {
            'name': '8',
            'title': 'Sex of news subjects (sources) inlocal,national,sub-regional/regional, foreign/intnl news',
            'desc': 'Breakdown by sex local,national,sub-regional/regional, intnl news',
            'reports': ['global', 'region', 'country'],
            'historical': '8',
        },
        '2010': {
            'name': '8',
            'title': 'Sex of news subjects (sources) inlocal,national,sub-regional/regional, foreign/intnl news',
            'desc': 'Breakdown by sex local,national,sub-regional/regional, intnl news',
            'reports': ['global', 'region', 'country'],
            'historical': '9cF',
        },
    },
    'ws_09': {
        '2015': {
            'name': '9',
            'title': 'Sex of news subjects in different story topics by GMMP year',
            'desc': 'Breakdown by sex & topic by GMMP year',
            'reports': ['global', 'region'],
            'historical': '9',
        },
        '2010': {
            'name': '9',
            'title': 'Sex of news subjects in different story topics',
            'desc': 'Breakdown of topic by sex',
            'reports': ['global', 'region'],
            'historical': '9dF',
        },
    },
    'ws_10': {
        '2015': {
            'name': '10',
            'title': 'Space allocated to major topics in Newspapers',
            'desc': 'Breakdown by major topic by space in newspapers',
            'reports': ['global', 'region', 'country'],
            'historical': '10',
        },
        '2010': {
            'name': '10',
            'title': 'Space allocated to major topics in Newspapers',
            'desc': 'Breakdown by major topic by space (q.4) in newspapers',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_11': {
        '2015': {
            'name': '11',
            'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by major topic',
            'desc': 'Breakdown by major topic by reference to gender equality/human rights/policy',
            'reports': ['global', 'region', 'country'],
            'historical': '11',
        },
        '2010': {
            'name': '11',
            'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by major topic',
            'desc': 'Breakdown by major topic by reference to gender equality/human rights/policy',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_12': {
        '2015': {
            'name': '12',
            'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by region',
            'desc': 'Breakdown by major topic by region by reference to gender equality/human rights/policy',
            'reports': ['global', 'region'],
            'historical': '12',
        },
        '2010': {
            'name': '12',
            'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by region',
            'desc': 'Breakdown by major topic by region by reference to gender equality/human rights/policy',
            'reports': ['global', 'region'],
        },
    },
    'ws_13': {
        '2015': {
            'name': '13',
            'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by sex of reporter',
            'desc': 'Breakdown by major topic by sex of reporter by reference to gender equality/human rights/policy',
            'reports': ['global', 'region',  'country'],
            'historical': '13',
        },
        '2010': {
            'name': '13',
            'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by sex of reporter',
            'desc': 'B.down by major topic by sex of reporter by reference to gender equality/human rights/policy',
            'reports': ['global', 'region',  'country'],
        },
    },
    'ws_14': {
        '2015': {
            'name': '14',
            'title': 'Position or occupation of news sources, by sex',
            'desc': 'Breakdown by sex and occupation',
            'reports': ['global', 'region', 'country'],
            'historical': '14',
        },
        '2010': {
            'name': '14',
            'title': 'Position or occupation of news sources, by sex',
            'desc': 'Breakdown of new sources by occupation and sex',
            'reports': ['global', 'region', 'country'],
            'historical': '9eF',
        },
    },
    'ws_15': {
        '2015': {
            'name': '15',
            'title': 'News subject\'s Function in news story, by sex',
            'desc': 'Breakdown by sex and function',
            'reports': ['global', 'region', 'country'],
            'historical': '15',
        },
        '2010': {
            'name': '15',
            'title': 'News subject\'s Function in news story, by sex',
            'desc': 'Breakdown by sex and function',
            'reports': ['global', 'region', 'country'],
            'historical': '9fF',
        },
    },
    'ws_16': {
        '2015': {
            'name': '16',
            'title': 'Function of news subjects by sex - by occupation',
            'desc': 'Breakdown of Function of news subjects by sex - by occupation',
            'reports': ['global', 'region', 'country'],
            'historical': '16',
        },
        '2010': {
            'name': '16',
            'title': 'Function of news subjects by sex - by occupation',
            'desc': 'Breakdown of  Function of news subjects by sex - by occupation',
            'reports': ['global', 'region', 'country'],
            'historical': '20aF',
        },
    },
    'ws_17': {
        '2015': {
            'name': '17',
            'title': 'Function of news subjects by sex - by age',
            'desc': 'Breakdown of  Function of news subjects by sex - by age',
            'reports': ['global', 'region', 'country'],
            'historical': '17',
        },
        '2010': {
            'name': '17',
            'title': 'Function of news subjects by sex - by age',
            'desc': 'Breakdown of  Function of news subjects by sex - by age',
            'reports': ['global', 'region', 'country'],
            'historical': '20bF',
        },
    },
    'ws_18': {
        '2015': {
            'name': '18',
            'title': 'Age of news subjects by print, by sex',
            'desc': 'B.down of  Age of news subjects by print, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '18',
        },
        '2010': {
            'name': '18',
            'title': 'Age of news subjects by print, by sex',
            'desc': 'B.down of  Age of news subjects by print, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '18cF',
        },
    },
    'ws_19': {
        '2015': {
            'name': '19',
            'title': 'Age of news subjects by broadcast, by sex',
            'desc': 'Breakdown of  Age of news subjects by broadcast, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '19',
        },
        '2010': {
            'name': '19',
            'title': 'Age of Television news subjects, by sex',
            'desc': 'B.down of  Age of Television news subjects, by sex (age captured for Television only)',
            'reports': ['global', 'region', 'country'],
            'historical': '18dF',
        },
    },
    'ws_20': {
        '2015': {
            'name': '20',
            'title': 'Functions (top 5) and Occupations by sex of news subject',
            'desc': 'Breakdown of  news subjects\' functions (top 5) and occupations by sex of news subject',
            'reports': ['global', 'region', 'country'],
            'historical': '20',
        },
        '2010': {
            'name': '20',
            'title': 'Functions and Occupations by sex of news subject',
            'desc': 'B.down of  news subjects\' functions and occupations by sex of news subject',
            'reports': ['global', 'region', 'country'],
            'historical': '20fF',
        },
    },
    'ws_21': {
        '2015': {
            'name': '21',
            'title': 'News Subjects who are portrayed as victims, by sex',
            'desc': 'Breakdown by victim type by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '21',
        },
        '2010': {
            'name': '21',
            'title': 'Breakdown by victim type by sex',
            'desc': 'News Subjects who are portrayed as victims, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '9gF',
        },
    },
    'ws_23': {
        '2015': {
            'name': '23',
            'title': 'News subjects who are portrayed as survivors, by sex',
            'desc': 'Breakdown of female & male news subjects who are survivors',
            'reports': ['global', 'region', 'country'],
            'historical': '23',
        },
        '2010': {
            'name': '23',
            'title': 'Breakdown by survivor type by sex',
            'desc': 'News subjects who are portrayed as survivors, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '19bF',
        },
    },
    'ws_24': {
        '2015': {
            'name': '24',
            'title': 'News subjects who are identified by family status, by sex.',
            'desc': 'Breakdown by sex, family status',
            'reports': ['global', 'region', 'country'],
            'historical': '24',
        },
        '2010': {
            'name': '24',
            'title': 'Breakdown by family status, by sex.',
            'desc': 'News subjects who are identified by family status, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '9hF',
        },
    },
    'ws_25': {
        '2015': {
            'name': '25',
            'title': 'News subjects who are identified by family status, by sex of news subject, by sex of reporter',
            'desc': 'Breakdown by sex of subject, family status, by sex of reporter',
            'reports': ['global', 'region', 'country'],
            'historical': '25',
        },
        '2010': {
            'name': '25',
            'title': 'B.down by sex of subject, family status, by sex of reporter',
            'desc': 'News subjects who are identified by family status, by sex of news subject, by sex of reporter',
            'reports': ['global', 'region', 'country'],
            'historical': '9kF',
        },
    },
    'ws_26': {
        '2015': {
            'name': '26',
            'title': 'News subjects quoted, by sex',
            'desc': 'Breakdown of  news subjects quoted, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '26',
        },
        '2010': {
            'name': '26',
            'title': 'Breakdown of  news subjects quoted, by sex',
            'desc': 'News subjects quoted, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '20gF',
        },
    },
    'ws_27': {
        '2015': {
            'name': '27',
            'title': 'News subjects photographed, by sex',
            'desc': 'Breakdown of news subjects photographed, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '27',
        },
        '2010': {
            'name': '27',
            'title': 'Breakdown of News subjects photographed, by sex',
            'desc': 'News subjects photographed, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '20hF',
        },
    },
    'ws_28': {
        '2015': {
            'name': '28',
            'title': 'Reporters, announcers and presenters all media, by region',
            'desc': 'Breakdown of reporters & presenters by region',
            'reports': ['global', 'region', 'country'],
            'historical': '28',
        },
        '2010': {
            'name': '28',
            'title': 'Breakdown of total female reporters & presenters by region by medium ',
            'desc': 'Female reporters, announcers and presenters all media, by region',
            'reports': ['global', 'region', 'country'],
            'historical': '10bF',
        },
    },
    'ws_28b': {
        '2015': {
            'name': '28b',
            'title': 'Breakdown of reporters  by region by medium PRINT RADIO TV INTERNET TWITTER by sex',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_28c': {
        '2015': {
            'name': '28c',
            'title': 'Breakdown of presenters  by region by medium by sex. TV and Radio',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_29': {
        '2015': {
            'name': '29',
            'title': 'Reporters in domestic & foreign stories (scope) , by region, by sex of reporter',
            'desc': 'Breakdown of Reporters in domestic & foreign stories, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '29',
        },
        '2010': {
            'name': '29',
            'title': 'Breakdown of female reporters in domestic & foreign stories, by region',
            'desc': 'Reporters in domestic & foreign stories (scope) , by region, by sex of reporter region',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_30': {
        '2015': {
            'name': '30',
            'title': 'Reporters, by sex on major topics, by region',
            'desc': 'Breakdown of Reporters, by sex on major topics',
            'reports': ['global', 'region', 'country'],
            'historical': '30',
        },
        '2010': {
            'name': '30',
            'title': 'Breakdown of female reporters, by major topic, by region',
            'desc': 'Reporters, by sex on major topics, by region',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_31': {
        '2015': {
            'name': '31',
            'title': 'Reporters, by sex on different topics - Detail',
            'desc': 'Breakdown of reporters, by sex on different topics - Detail',
            'reports': ['global'],
            'historical': '31',
        },
        '2010': {
            'name': '31',
            'title': 'Breakdown of Reporters, by sex on different topics - Detail',
            'desc': 'Rporters, by sex on different topics - Detail',
            'reports': ['global'],
            'historical': '12dF',
        },
    },
    'ws_32': {
        '2015': {
            'name': '32',
            'title': 'Topics in the news - Detail  by medium, by sex of reporter',
            'desc': 'Breakdown of news topics by medium by sex of reporter',
            'reports': ['global', 'region', 'country'],
            'historical': '32',
        },
        '2010': {
            'name': '32',
            'title': 'Topics in the news - Detail by medium for female reporters',
            'desc': 'Topics in the news - Detail by medium for female reporters',
            'reports': ['global'],
        },
    },
    'ws_34': {
        '2015': {
            'name': '34',
            'title': 'Selection of News Subject(sex of source)  by female & male reporters',
            'desc': 'Breakdown of News Subject (sex of source) selection  by female & male reporters',
            'reports': ['global', 'region', 'country'],
            'historical': '34',
        },
        '2010': {
            'name': '34',
            'title': 'Breakdown of News Subject (sex of source) selection by female & male reporters',
            'desc': 'Selection of News Subject (sex of source, in rows) by female & male reporters (in columns)',
            'reports': ['global', 'region', 'country'],
            'historical': '13bF',
        },
    },
    'ws_35': {
        '2015': {
            'name': '35',
            'title': 'Breakdown of television Announcers & Reporters, by age, by sex',
            'desc': 'Age of television Announcers & Reporters, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '35',
        },
        '2010': {
            'name': '35',
            'title': 'Breakdown of television Announcers & Reporters, by age, by sex',
            'desc': 'Age of television Announcers & Reporters, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '14F',
        },
    },
    'ws_36': {
        '2015': {
            'name': '36',
            'title': 'Age of television Announcers & Reporters, by sex',
            'desc': 'Breakdown of television Announcers & Reporters, by age, by sex',
            'reports': ['global', 'region', 'country'],
            'historical': '36',
        },
        '2010': {
            'name': '36',
            'title': 'Breakdown of Stories with Women as central focus (is this story about a particular woman or women) by sex of reporter',
            'desc': 'Stories with Women as central focus  by sex of reporter',
            'reports': ['global', 'region', 'country'],
            'historical': '15aF',
        },
    },
    'ws_38': {
        '2015': {
            'name': '38',
            'title': 'Stories with Women as a central Focus by major topic',
            'desc': 'Breakdown of Stories with Women as a central Focus by major topic',
            'reports': ['global', 'region', 'country'],
            'historical': '38',
        },
        '2010': {
            'name': '38',
            'title': 'Breakdown of Stories with Women as a central Focus by major topic',
            'desc': 'Stories with Women as a central Focus by major topic',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_39': {
        '2015': {
            'name': '39',
            'title': 'Stories with Women as a central Focus by minor topic',
            'desc': 'Breakdown of Stories with Women as a central Focus by minor topic',
            'reports': ['global'],
            'historical': '39',
        },
        '2010': {
            'name': '39',
            'title': 'Breakdown of Stories with Women as a central Focus by minor topic',
            'desc': 'Stories with Women as a central Focus by minor topic',
            'reports': ['global'],
            'historical': '15bF',
        },
    },
    'ws_40': {
        '2015': {
            'name': '40',
            'title': 'Stories with Women as a central Focus by topic and region',
            'desc': 'Breakdown of Stories with Women as a central Focus by topic and region',
            'reports': ['global'],
            'historical': '40',
        },
        '2010': {
            'name': '40',
            'title': 'Breakdown of Stories with Women as a central Focus by topic and region',
            'desc': 'Stories with Women as a central Focus by topic and region',
            'reports': ['global'],
            'historical': '15cF',
        },
    },
    'ws_41': {
        '2015': {
            'name': '41',
            'title': 'Stories where issues of gender equality/inequality are raised by topic',
            'desc': 'Breakdown of  Stories where issues of gender equality/inequality are raised by topic',
            'reports': ['global', 'region', 'country'],
            'historical': '41',
        },
    },
    'ws_42': {
        '2015': {
            'name': '42',
            'title': 'Stories where issues of gender equality/inequality are raised by region',
            'desc': '',
            'reports': ['global'],
            'historical': '42',
        },
    },
    'ws_43': {
        '2015': {
            'name': '43',
            'title': 'Stories where issues of gender equality/inequality are raised by sex of reporter',
            'desc': 'Breakdown of Stories where issues of gender equality/inequality are raised by sex of reporter',
            'reports': ['global', 'region', 'country'],
            'historical': '43',
        },
        '2010': {
            'name': '43',
            'title': 'Breakdown of Stories where issues of gender equality/inequality are raised by sex of reporter',
            'desc': 'Stories where issues of gender equality/inequality are raised by sex of reporter',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_44': {
        '2015': {
            'name': '44',
            'title': 'Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
            'desc': 'Breakdown of Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
            'reports': ['global', 'region'],
            'historical': '44',
        },
        '2010': {
            'name': '44',
            'title': 'Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
            'desc': 'Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
            'reports': ['global', 'region'],
            'historical': '16cF',
        },
    },
    'ws_45': {
        '2015': {
            'name': '45',
            'title': 'Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
            'desc': 'Breakdown of Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
            'reports': ['global', 'region'],
            'historical': '45',
        },
        '2010': {
            'name': '45',
            'title': 'Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
            'desc': 'Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
            'reports': ['global', 'region'],
            'historical': '16dF',
        },
    },
    'ws_46': {
        '2015': {
            'name': '46',
            'title': 'Stories where stereotypes are challenged/ supported by news topic',
            'desc': 'Breakdown of Stories where stereotypes are challenged/ supported by news topic',
            'reports': ['global'],
            'historical': '46',
        },
        '2010': {
            'name': '46',
            'title': 'Story clearly challenges gender stereotypes by region by major news topic',
            'desc': 'Stories where stereotypes are challenged/ supported by news topic',
            'reports': ['global'],
        },
    },
    'ws_47': {
        '2015': {
            'name': '47',
            'title': 'Stories where stereotypes are challenged/ supported by region',
            'desc': 'Breakdown of  Stories where stereotypes are challenged/ supported by region',
            'reports': ['global', 'region', 'country'],
            'historical': '47',
        },
        '2010': {
            'name': '47',
            'title': 'Story clearly challenges gender stereotypes by major topic',
            'desc': 'Stories where stereotypes are challenged/ supported by topic',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_48': {
        '2015': {
            'name': '48',
            'title': 'Stories where stereotypes are challenged/ supported by gender of rep',
            'desc': 'Breakdown of  Stories where stereotypes are challenged/ supported by gender of rep',
            'reports': ['global', 'region', 'country'],
            'historical': '48',
        },
        '2010': {
            'name': '48',
            'title': 'Story clearly challenges gender stereotypes by sex of rep',
            'desc': 'Stories where stereotypes are challenged/ supported by gender of rep',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_49': {
        '2015': {
            'name': '49',
            'title': 'Internet - Main topics by region',
            'desc': 'Breakdown of main topics in internet news by sex of news subjects',
            'reports': ['global', 'region'],
            'historical': '49',
        },
        '2010': {
            'name': '49',
            'title': 'Internet - Main topics by region',
            'desc': 'Internet - Main topics by region',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_50': {
        '2015': {
            'name': '50',
            'title': 'Internet - Story shared on Twitter',
            'desc': '',
            'reports': ['global', 'country'],
            'historical': '50',
        },
        '2010': {
            'name': '50',
            'title': 'Internet - Story shared on Twitter',
            'desc': '',
            'reports': ['global', 'country'],
        },
    },
    'ws_51': {
        '2015': {
            'name': '51',
            'title': 'Internet - Story shared on Facebook',
            'desc': '',
            'reports': ['global', 'country'],
            'historical': '51',
        },
        '2010': {
            'name': '51',
            'title': 'Internet - Story shared on Facebook',
            'desc': '',
            'reports': ['global', 'country'],
        },
    },
    'ws_52': {
        '2015': {
            'name': '52',
            'title': 'Internet - Reference to gender equality/HR policies',
            'desc': '',
            'reports': ['global', 'country'],
            'historical': '52',
        },
        '2010': {
            'name': '52',
            'title': 'Internet - Reference to gender equality/HR policies',
            'desc': '',
            'reports': ['global', 'country'],
        },
    },
    'ws_53': {
        '2015': {
            'name': '53',
            'title': 'Internet - Female reporters in main stories',
            'desc': 'Internet - Sex of reporters in main stories',
            'reports': [],
            'historical': '53',
        },
    },
    'ws_54': {
        '2015': {
            'name': '54',
            'title': 'Internet - Overall presence of women',
            'desc': '',
            'reports': [],
            'historical': '54',
        },
    },
    'ws_55': {
        '2015': {
            'name': '55',
            'title': 'Internet, Twitter  - Occupation of Female news subjects',
            'desc': 'Breakdown Internet, Twitter - Occupation and function by sex of News Subjects',
            'reports': ['global', 'region', 'country'],
            'historical': '55',
        },
    },
    'ws_56': {
        '2015': {
            'name': '56',
            'title': 'Internet, Twitter - Functions of news subjects',
            'desc': '',
            'reports': ['global', 'region', 'country'],
            'historical': '56',
        },
        '2010': {
            'name': '56',
            'title': 'Internet - Functions of news subjects',
            'desc': 'Internet - Functions of news subjects',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_57': {
        '2015': {
            'name': '57',
            'title': 'Internet - News subjects who are identified by family status',
            'desc': 'Internet - News subjects, by sex, who are identified by family status',
            'reports': ['global', 'country'],
            'historical': '57',
        },
        '2010': {
            'name': '57',
            'title': 'Internet - News subjects who are identified by family status',
            'desc': 'Internet - News subjects who are identified by family status',
            'reports': ['global', 'country'],

        },
    },
    'ws_58': {
        '2015': {
            'name': '58',
            'title': 'Internet - News subjects in multimedia web components',
            'desc': 'Internet - Sex of news subjects in multimedia components and photographs',
            'reports': ['global', 'country'],
            'historical': '58',
        },
        '2010': {
            'name': '58',
            'title': 'Internet - News subjects in multimedia web components',
            'desc': 'Internet - News subjects in multimedia web components',
            'reports': ['global', 'country'],
        },
    },
    'ws_59': {
        '2015': {
            'name': '59',
            'title': 'Internet - Selection of News Subjects',
            'desc': 'Internet - Selection of News Subjects by sex of reporter (columns) and sex of subject (rows)',
            'reports': ['global', 'country'],
            'historical': '59',
        },
        '2010': {
            'name': '59',
            'title': 'Internet - Selection of News Subjects',
            'desc': 'Internet - Selection of News Subjects by sex of reporter (columns) and sex of subject (rows)',
            'reports': ['global', 'country'],
        },
    },
    'ws_60': {
        '2015': {
            'name': '60',
            'title': 'Internet - Age of news subjects',
            'desc': 'Internet - Age of news subjects by sex',
            'reports': ['global', 'country'],
            'historical': '60',
        },
        '2010': {
            'name': '60',
            'title': 'Internet - Age of news subjects',
            'desc': 'Internet - Age of news subjects',
            'reports': ['global', 'country'],
        },
    },
    'ws_61': {
        '2015': {
            'name': '61',
            'title': 'Internet - News subjects who are directly quoted',
            'desc': 'Internet - News subjects directly quoted by sex',
            'reports': ['global', 'country'],
            'historical': '61',
        },
        '2010': {
            'name': '61',
            'title': 'Internet - News subjects who are directly quoted',
            'desc': 'Internet - News subjects who are directly quoted',
            'reports': ['global', 'country'],
        },
    },
    'ws_62': {
        '2015': {
            'name': '62',
            'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
            'desc': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
            'reports': ['global', 'region', 'country'],
            'historical': '62',
        },
        '2010': {
            'name': '62',
            'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
            'desc': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_63': {
        '2015': {
            'name': '63',
            'title': 'Internet -Stories where stereotypes are clearly challenged',
            'desc': 'Internet -Stories where stereotypes are clearly challenged',
            'reports': ['global', 'region', 'country'],
            'historical': '63',
        },
        '2010': {
            'name': '63',
            'title': 'Internet -Stories where stereotypes are clearly challenged',
            'desc': 'Internet -Stories where stereotypes are clearly challenged',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_64': {
        '2015': {
            'name': '64',
            'title': 'Internet -Stories with Women as a central Focus',
            'desc': 'Internet -Stories with Women as a central Focus',
            'reports': ['global', 'region', 'country'],
            'historical': '64',
        },
        '2010': {
            'name': '64',
            'title': 'Internet -Stories with Women as a central Focus',
            'desc': 'Internet -Stories with Women as a central Focus',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_65': {
        '2015': {
            'name': '65',
            'title': 'Twitter - Original tweet or retweet',
            'desc': '',
            'reports': ['global', 'region', 'country'],
            'historical': '65',
        },
        '2010': {
            'name': '65',
            'title': 'Twitter - Original tweet or retweet',
            'desc': 'Twitter - Original tweet or retweet',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_66': {
        '2015': {
            'name': '66',
            'title': 'Twitter - Overall presence of women',
            'desc': '',
            'reports': [],
            'historical': '66',
        },
        '2010': {
            'name': '66',
            'title': 'Twitter - Overall presence of women',
            'desc': 'Twitter - Overall presence of women',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_67': {
        '2015': {
            'name': '67',
            'title': 'Twitter - Female reporters & journalists',
            'desc': '',
            'reports': [],
            'historical': '67',
        },
        '2010': {
            'name': '67',
            'title': 'Twitter - Female reporters & journalists',
            'desc': 'Twitter - Female reporters & journalists',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_68': {
        '2015': {
            'name': '68',
            'title': 'Twitter - Women\'s centrality',
            'desc': '',
            'reports': [],
            'historical': '68',
        },
        '2010': {
            'name': '68',
            'title': 'Twitter - Women\'s centrality',
            'desc': 'Twitter - Women\'s centrality',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_68b': {
        '2015': {
            'name': '68b',
            'title': 'Twitter - Challenging Stereotypes',
            'desc': 'Twitter - This tweet clearly challenges gender stereotypes, by major topic',
            'reports': ['global', 'region', 'country'],
            'historical': '68b',
        },
        '2010': {
            'name': '68b',
            'title': 'Twitter - Challenging Stereotypes',
            'desc': 'Twitter - Challenging Stereotypes',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_70': {
        '2010': {
            'name': '70',
            'title': 'Twitter - Hashtags',
            'desc': 'Twitter - Hashtags',
            'reports': ['global'],
        },
    },
    'ws_71': {
        '2015': {
            'name': '71',
            'title': 'Key themes, women\'s overall presence',
            'desc': '',
            'reports': [],
            'historical': '71',
        },
        '2010': {
            'name': '71',
            'title': 'Key themes, women\'s overall presence',
            'desc': 'Key themes, women\'s overall presence',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_72': {
        '2015': {
            'name': '72',
            'title': 'Key themes, female reporters',
            'desc': '',
            'reports': [],
            'historical': '72',
        },
        '2010': {
            'name': '72',
            'title': 'Key themes, female reporters',
            'desc': 'Key themes, female reporters',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_73': {
        '2015': {
            'name': '73',
            'title': 'Key themes, selection of sources by sex of reporter',
            'desc': '',
            'reports': [],
            'historical': '73',
        },
        '2010': {
            'name': '73',
            'title': 'Key themes, selection of sources by sex of reporter',
            'desc': 'Key themes, selection of sources by sex of reporter',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_74': {
        '2015': {
            'name': '74',
            'title': 'Key themes, women\'s centrality',
            'desc': '',
            'reports': [],
            'historical': '74',
        },
        '2010': {
            'name': '74',
            'title': 'Key themes, women\'s centrality',
            'desc': 'Stories with Women as a central focus, by women centrality topic',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_75': {
        '2015': {
            'name': '75',
            'title': 'Key themes, challenging stereotypes',
            'desc': '',
            'reports': [],
            'historical': '75',
        },
        '2010': {
            'name': '75',
            'title': 'Key themes, challenging stereotypes',
            'desc': 'Key themes, challenging stereotypes',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_76': {
        '2015': {
            'name': '76',
            'title': 'Key themes, reference to gender equality/HR policies',
            'desc': '',
            'reports': [],
            'historical': '76',
        },
        '2010': {
            'name': '76',
            'title': 'Key themes, reference to gender equality/HR policies',
            'desc': 'Key themes, reference to gender equality/HR policies',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_77': {
        '2015': {
            'name': '77',
            'title': 'Key themes, portrayal as victims',
            'desc': '',
            'reports': [],
            'historical': '77',
        },
        '2010': {
            'name': '77',
            'title': 'Key themes, portrayal as victims',
            'desc': 'Key themes, portrayal as victims',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_78': {
        '2015': {
            'name': '78',
            'title': 'Key themes, portrayal as survivors',
            'desc': '',
            'reports': [],
            'historical': '78',
        },
        '2010': {
            'name': '78',
            'title': 'Key themes, portrayal as survivors',
            'desc': 'Key themes, portrayal as survivors',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_79': {
        '2015': {
            'name': '79',
            'title': 'Internet - Main topics by region',
            'desc': 'Breakdown by sex of news subjects',
            'reports': ['global'],
            'historical': '79',
        },
        '2010': {
            'name': '79',
            'title': 'Internet - Main topics by region',
            'desc': 'Internet - Main topics by region',
            'reports': ['global'],
        },
    },
    'ws_80': {
        '2015': {
            'name': '80',
            'title': 'Internet - Story shared on Twitter',
            'desc': 'Breakdown by major and minor topics',
            'reports': ['global'],
            'historical': '80',
        },
        '2010': {
            'name': '80',
            'title': 'Internet - Story shared on Twitter',
            'desc': 'Internet - Story shared on Twitter',
            'reports': ['global'],
        }
    },
    'ws_81': {
        '2015': {
            'name': '81',
            'title': 'Internet - Story shared on Facebook',
            'desc': 'Breakdown by major and minor topics',
            'reports': ['global'],
            'historical': '81',
        },
        '2010': {
            'name': '81',
            'title': 'Internet - Story shared on Facebook',
            'desc': 'Internet - Story shared on Facebook',
            'reports': ['global'],
        },
    },
    'ws_82': {
        '2015': {
            'name': '82',
            'title': 'Internet - Reference to gender equality/HR policies',
            'desc': 'Breakdown by major and minor topics',
            'reports': ['global'],
            'historical': '82',
        },
        '2010': {
            'name': '82',
            'title': 'Internet - Reference to gender equality/HR policies',
            'desc': 'Internet - Reference to gender equality/HR policies',
            'reports': ['global'],
        },
    },
    'ws_83': {
        '2015': {
            'name': '83',
            'title': 'Internet - reporters in main stories',
            'desc': 'Breakdown by major topic',
            'reports': ['global'],
            'historical': '83',
        },
        '2010': {
            'name': '83',
            'title': 'Internet - reporters in main stories',
            'desc': 'Internet - reporters in main stories',
            'reports': ['global'],
        },
    },
    'ws_84': {
        '2015': {
            'name': '84',
            'title': 'Internet - Occupation of Female news subjects',
            'desc': '',
            'reports': ['global'],
            'historical': '84',
        },
        '2010': {
            'name': '84',
            'title': 'Internet - Occupation of Female news subjects',
            'desc': 'Internet - Occupation of Female news subjects',
            'reports': ['global'],
        },
    },
    'ws_85': {
        '2015': {
            'name': '85',
            'title': 'Internet - Functions of news subjects',
            'desc': '',
            'reports': ['global'],
            'historical': '85',
        },
        '2010': {
            'name': '85',
            'title': 'Internet - Functions of news subjects',
            'desc': 'Internet - Functions of news subjects',
            'reports': ['global'],
        },
    },
    'ws_86': {
        '2015': {
            'name': '86',
            'title': 'Internet - News subjects who are identified by family status',
            'desc': '',
            'reports': ['global'],
            'historical': '86',
        },
        '2010': {
            'name': '86',
            'title': 'Internet - News subjects who are identified by family status',
            'desc': 'Internet - News subjects who are identified by family status',
            'reports': ['global'],
        },
    },
    'ws_87': {
        '2015': {
            'name': '87',
            'title': 'Internet - News subjects in multimedia web components',
            'desc': '',
            'reports': ['global'],
            'historical': '87',
        },
        '2010': {
            'name': '87',
            'title': 'Internet - News subjects in multimedia web components',
            'desc': 'Internet - News subjects in multimedia web components',
            'reports': ['global'],
        },
    },
    'ws_88': {
        '2015': {
            'name': '88',
            'title': 'Internet - Selection of News Subjects',
            'desc': 'Breakdown by sex of reporter',
            'reports': ['global'],
            'historical': '88',
        },
        '2010': {
            'name': '88',
            'title': 'Internet - Selection of News Subjects',
            'desc': 'Internet - Selection of News Subjects',
            'reports': ['global'],
        }
    },
    'ws_89': {
        '2015': {
            'name': '89',
            'title': 'Internet - Age of news subjects',
            'desc': 'Breakdown by sex',
            'reports': ['global'],
            'historical': '89',
        },
        '2010': {
            'name': '89',
            'title': 'Internet - Age of news subjects',
            'desc': 'Internet - Age of news subjects',
            'reports': ['global'],
        },
    },
    'ws_90': {
        '2015': {
            'name': '90',
            'title': 'Internet - News subjects who are directly quoted',
            'desc': 'Breakdown by sex',
            'reports': ['global'],
            'historical': '90',
        },
        '2010': {
            'name': '90',
            'title': 'Internet - News subjects who are directly quoted',
            'desc': 'Internet - News subjects who are directly quoted',
            'reports': ['global'],
        },
    },
    'ws_91': {
        '2015': {
            'name': '91',
            'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
            'desc': '',
            'reports': ['global'],
            'historical': '91',
        },
        '2010': {
            'name': '91',
            'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
            'desc': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
            'reports': ['global'],
        },
    },
    'ws_92': {
        '2015': {
            'name': '92',
            'title': 'Internet -Stories where stereotypes are clearly challenged',
            'desc': 'Breakdown by major topic',
            'reports': ['global'],
            'historical': '92',
        },
        '2010': {
            'name': '92',
            'title': 'Internet -Stories where stereotypes are clearly challenged',
            'desc': 'Internet -Stories where stereotypes are clearly challenged',
            'reports': ['global'],
        },
    },
    'ws_93': {
        '2015': {
            'name': '93',
            'title': 'Internet -Stories with Women as a central Focus',
            'desc': 'Breakdown by major topic',
            'reports': ['global'],
            'historical': '93',
        },
        '2010': {
            'name': '93',
            'title': 'Internet -Stories with Women as a central Focus',
            'desc': 'Internet -Stories with Women as a central Focus',
            'reports': ['global'],
        },
    },
    'ws_94': {
        '2015': {
            'name': '94',
            'title': 'Twitter - Original tweet or retweet',
            'desc': 'Breakdown by major topic',
            'reports': ['global'],
            'historical': '94',
        },
        '2010': {
            'name': '94',
            'title': 'Twitter - Original tweet or retweet',
            'desc': 'Twitter - Original tweet or retweet',
            'reports': ['global'],
        },
    },
    'ws_95': {
        '2015': {
            'name': '95',
            'title': 'Twitter - Female reporters',
            'desc': 'Breakdown by major topic',
            'reports': ['global'],
            'historical': '95',
        },
        '2010': {
            'name': '95',
            'title': 'Twitter - Female reporters',
            'desc': 'Twitter - Female reporters',
            'reports': ['global'],
        },
    },
    'ws_96': {
        '2015': {
            'name': '96',
            'title': 'Twitter - Women\'s centrality',
            'desc': 'Breakdown by major topic',
            'reports': ['global'],
            'historical': '96',
        },
        '2010': {
            'name': '96',
            'title': 'Twitter - Women\'s centrality',
            'desc': 'Twitter - Women\'s centrality',
            'reports': ['global'],
        },
    },
    'ws_97': {
        '2015': {
            'name': '97',
            'title': 'Twitter - Challenging Stereotypes',
            'desc': 'Breakdown by major topic',
            'reports': ['global'],
            'historical': '97',
        },
        '2010': {
            'name': '97',
            'title': 'Twitter - Challenging Stereotypes',
            'desc': 'Twitter - Challenging Stereotypes',
            'reports': ['global'],
        },
    },
    'ws_98': {
        '2015': {
            'name': '98',
            'title': 'Twitter - Images',
            'desc': '',
            'historical': '98',
            'reports': [],
        },
    },
    'ws_100': {
        '2015': {
            'name': '100',
            'title': 'Is this story related to Covid19. By major topic, by medium',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_101': {
        '2015': {
            'name': '101',
            'title': 'Covid stories:  reporters, by sex',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_102': {
        '2015': {
            'name': '102',
            'title': 'Covid stories: gender stereotypes, by major topic',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_103': {
        '2015': {
            'name': '103',
            'title': 'Covid stories: highlight gender inequalities, by major topic',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_104': {
        '2015': {
            'name': '104',
            'title': 'Covid stories:  news subjects and sources, by function in the news, by sex',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_105': {
        '2015': {
            'name': '105',
            'title': 'Covid stories:  news subjects and sources, survivors by sex',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_106': {
        '2015': {
            'name': '106',
            'title': 'Covid stories: news subjects and sources, occupation by sex',
            'desc': '',
            'reports': ['global', 'region', 'country'],
        },
    },
    'ws_107': {
        '2015': {
            'name': '107',
            'title': 'Special questions, by major topic, by medium',
            'desc': '',
            'reports': ['country'],
        },
    },
    'ws_108': {
        '2015': {
            'name': '108',
            'title': 'Special questions, by major topic, by sex of source',
            'desc': '',
            'reports': ['country'],
        },
    },
    'ws_109': {
        '2015': {
            'name': '109',
            'title': 'Special questions, by major topic, by reporter',
            'desc': '',
            'reports': ['country'],
        },
    },
    'ws_110': {
        '2015': {
            'name': '110',
            'title': 'Special questions, by major topic, by rights/policy',
            'desc': '',
            'reports': ['country'],
        },
    },
    'ws_111': {
        '2015': {
            'name': '111',
            'title': 'Special questions, by major topic, by gender stereotypes',
            'desc': '',
            'reports': ['country'],
        },
    },
    'ws_s01': {
        '2015': {
            'name': 's01',
            'title': 'Sex of presenters, reporters and news subjects',
            'desc': 'Sex of presenters, reporters and news subjects',
            'reports': ['global'],
            'historical': 's01',
        },
        '2010': {
            'name': 's01',
            'title': 'Sex of presenters, reporters and news subjects',
            'desc': 'Sex of presenters, reporters and news subjects',
            'reports': ['global'],
        },
    },
    'ws_s02': {
        '2015': {
            'name': 's02',
            'title': 'News subjects in television, radio and newspapers',
            'desc': 'News subjects in television, radio and newspapers',
            'reports': ['global'],
            'historical': 's02',
        },
        '2010': {
            'name': 's02',
            'title': 'News subjects in television, radio and newspapers',
            'desc': 'News subjects in television, radio and newspapers',
            'reports': ['global'],
        },
    },
    'ws_s03': {
        '2015': {
            'name': 's03',
            'title': 'News subjects in major topic areas',
            'desc': 'News subjects in major topic areas',
            'reports': ['global'],
            'historical': 's03',
        },
        '2010': {
            'name': 's03',
            'title': 'News subjects in major topic areas',
            'desc': 'News subjects in major topic areas',
            'reports': ['global'],
        },
    },
    'ws_s04': {
        '2015': {
            'name': 's04',
            'title': 'News subjects in major occupational groups',
            'desc': 'News subjects in major occupational groups',
            'reports': ['global'],
            'historical': 's04',
        },
        '2010': {
            'name': 's04',
            'title': 'News subjects in major occupational groups',
            'desc': 'News subjects in major occupational groups',
            'reports': ['global'],
        },
    },
    'ws_s05': {
        '2015': {
            'name': 's05',
            'title': 'Function of news subjects',
            'desc': 'Function of news subjects',
            'reports': ['global'],
            'historical': 's05',
        },
        '2010': {
            'name': 's05',
            'title': 'Function of news subjects',
            'desc': 'Function of news subjects',
            'reports': ['global'],
        },
    },
    'ws_s06': {
        '2015': {
            'name': 's06',
            'title': 'News subjects who are victims',
            'desc': '',
            'reports': ['global'],
            'historical': 's06',
        },
        '2010': {
            'name': 's06',
            'title': 'News subjects who are victims',
            'desc': 'News subjects who are victims',
            'reports': ['global'],
        },
    },
    'ws_s07': {
        '2015': {
            'name': 's07',
            'title': 'News subjects mentioned by family status',
            'desc': 'News subjects mentioned by family status',
            'reports': ['global'],
            'historical': 's07',
        },
        '2010': {
            'name': 's07',
            'title': 'News subjects mentioned by family status',
            'desc': 'News subjects mentioned by family status',
            'reports': ['global'],
        },
    },
    'ws_s08': {
        '2015': {
            'name': 's08',
            'title': 'News subjects quoted in newspapers',
            'desc': 'News subjects quoted in newspapers',
            'reports': ['global'],
            'historical': 's08',
        },
        '2010': {
            'name': 's08',
            'title': 'News subjects quoted in newspapers',
            'desc': 'News subjects quoted in newspapers',
            'reports': ['global'],
        },
    },
    'ws_s09': {
        '2015': {
            'name': 's09',
            'title': 'Print only - News subjects appearing in newspaper photographs',
            'desc': 'Print only - News subjects appearing in newspaper photographs',
            'reports': ['global'],
            'historical': 's09',
        },
        '2010': {
            'name': 's09',
            'title': 'Print only - News subjects appearing in newspaper photographs',
            'desc': 'Print only - News subjects appearing in newspaper photographs',
            'reports': ['global'],
        },
    },
    'ws_s10': {
        '2015': {
            'name': 's10',
            'title': 'Presenters and reporters in television, radio and newspapers',
            'desc': '',
            'reports': ['global'],
            'historical': 's10',
        },
        '2010': {
            'name': 's10',
            'title': 'Presenters and reporters in television, radio and newspapers',
            'desc': 'Presenters and reporters in television, radio and newspapers',
            'reports': ['global'],
        },
    },
    'ws_s11': {
        '2015': {
            'name': 's11',
            'title': 'Reporters in major topic areas',
            'desc': 'Reporters in major topic areas',
            'reports': ['global'],
            'historical': 's11',
        },
        '2010': {
            'name': 's11',
            'title': 'Reporters in major topic areas',
            'desc': 'Reporters in major topic areas',
            'reports': ['global'],
        },
    },
    'ws_s12': {
        '2015': {
            'name': 's12',
            'title': 'Topics in stories where women are central to the news',
            'desc': 'Topics in stories where women are central to the news',
            'reports': ['global'],
            'historical': 's12',
        },
        '2010': {
            'name': 's12',
            'title': 'Topics in stories where women are central to the news',
            'desc': 'Topics in stories where women are central to the news',
            'reports': ['global'],
        },
    },
    'ws_s13': {
        '2015': {
            'name': 's13',
            'title': 'Sex of reporter in stories with female and male news subjects',
            'desc': 'Sex of reporter in stories with female and male news subjects',
            'reports': ['global'],
            'historical': 's13',
        },
        '2010': {
            'name': 's13',
            'title': 'Sex of reporter in stories with female and male news subjects',
            'desc': 'Sex of reporter in stories with female and male news subjects',
            'reports': ['global'],
        }
    },
    'ws_s14': {
        '2015': {
            'name': 's14',
            'title': 'Stories that clearly challenge stereotypes',
            'desc': 'Stories that clearly challenge stereotypes',
            'reports': ['global'],
            'historical': 's14',
        },
        '2010': {
            'name': 's14',
            'title': 'Stories that clearly challenge stereotypes',
            'desc': 'Stories that clearly challenge stereotypes',
            'reports': ['global'],
        },
    },
    'ws_s15': {
        '2015': {
            'name': 's15',
            'title': 'Stories that highlight gender equality or inequality',
            'desc': 'Stories that highlight gender equality or inequality',
            'reports': ['global'],
            'historical': 's15',
        },
        '2010': {
            'name': 's15',
            'title': 'Stories that highlight gender equality or inequality',
            'desc': 'Stories that highlight gender equality or inequality',
            'reports': ['global'],
        },
    },
    'ws_s16': {
        '2015': {
            'name': 's16',
            'title': 'Stories that mention human rights or equality legislation and policies',
            'desc': 'Stories that mention human rights or equality legislation and policies',
            'reports': ['global'],
            'historical': 's16',
        },
        '2010': {
            'name': 's16',
            'title': 'Stories that mention human rights or equality legislation and policies',
            'desc': 'Stories that mention human rights or equality legislation and policies',
            'reports': ['global'],
        },
    },
    'ws_s17': {
        '2015': {
            'name': 's17',
            'title': 'Internet, Twitter - Sex of reporters and news subjects',
            'desc': 'Internet, Twitter - Sex of reporters and news subjects',
            'reports': ['global'],
            'historical': 's17',
        },
        '2010': {
            'name': 's17',
            'title': 'Internet, Twitter - Sex of reporters and news subjects',
            'desc': 'Internet, Twitter - Sex of reporters and news subjects',
            'reports': ['global'],
        },
    },
    'ws_s18': {
        '2015': {
            'name': 's18',
            'title': 'Internet, Twitter - News subjects on Internet and Twitter news',
            'desc': 'Internet, Twitter - News subjects on Internet and Twitter news',
            'reports': ['global'],
            'historical': 's18',
        },
        '2010': {
            'name': 's18',
            'title': 'Internet, Twitter - News subjects on Internet and Twitter news',
            'desc': 'Internet, Twitter - News subjects on Internet and Twitter news',
            'reports': ['global'],
        },
    },
    'ws_s19': {
        '2015': {
            'name': 's19',
            'title': 'Internet, Twitter - News subjects in major topic areas',
            'desc': 'Internet, Twitter - News subjects in major topic areas',
            'reports': ['global'],
            'historical': 's19',
        },
        '2010': {
            'name': 's19',
            'title': 'Internet, Twitter - News subjects in major topic areas',
            'desc': 'Internet, Twitter - News subjects in major topic areas',
            'reports': ['global'],
        },
    },
    'ws_s20': {
        '2015': {
            'name': 's20',
            'title': 'Internet - News subjects in major occupational groups',
            'desc': 'Internet - News subjects in major occupational groups',
            'reports': ['global'],
            'historical': 's20',
        },
        '2010': {
            'name': 's20',
            'title': 'Internet - News subjects in major occupational groups',
            'desc': 'Internet - News subjects in major occupational groups',
            'reports': ['global'],
        },
    },
    'ws_s21': {
        '2015': {
            'name': 's21',
            'title': 'Internet - Function of news subjects',
            'desc': 'Internet - Function of news subjects',
            'reports': ['global'],
            'historical': 's21',
        },
        '2010': {
            'name': 's21',
            'title': 'Internet - Function of news subjects',
            'desc': 'Internet - Function of news subjects',
            'reports': ['global'],
        },
    },
    'ws_s22': {
        '2015': {
            'name': 's22',
            'title': 'Internet - News subjects who are victims',
            'desc': 'Internet - News subjects who are victims',
            'reports': ['global'],
            'historical': 's22',
        },
        '2010': {
            'name': 's22',
            'title': 'Internet - News subjects who are victims',
            'desc': 'Internet - News subjects who are victims',
            'reports': ['global'],
        },
    },
    'ws_s23': {
        '2015': {
            'name': 's23',
            'title': 'Internet - News subjects quoted',
            'desc': 'Internet - News subjects quoted',
            'reports': ['global'],
            'historical': 's23',
        },
        '2010': {
            'name': 's23',
            'title': 'Internet - News subjects quoted',
            'desc': 'Internet - News subjects quoted',
            'reports': ['global'],
        },
    },
    'ws_s24': {
        '2015': {
            'name': 's24',
            'title': 'Internet, Twitter - News subjects appearing in images and video plug-ins',
            'desc': 'Internet, Twitter - News subjects appearing in images and video plug-ins',
            'reports': ['global'],
            'historical': 's24',
        },
        '2010': {
            'name': 's24',
            'title': 'Internet, Twitter - News subjects appearing in images and video plug-ins',
            'desc': 'Internet, Twitter - News subjects appearing in images and video plug-ins',
            'reports': ['global'],
        },
    },
    'ws_s25': {
        '2015': {
            'name': 's25',
            'title': 'Internet, Twitter - Reporters in major topic areas',
            'desc': 'Internet, Twitter - Reporters in major topic areas',
            'reports': ['global'],
            'historical': 's25',
        },
        '2010': {
            'name': 's25',
            'title': 'Internet, Twitter - Reporters in major topic areas',
            'desc': 'Internet, Twitter - Reporters in major topic areas',
            'reports': ['global'],
        },
    },
    'ws_s26': {
        '2015': {
            'name': 's26',
            'title': 'Internet, Twitter - Topics in stories where women are central to the news',
            'desc': 'Internet, Twitter - Topics in stories where women are central to the news',
            'reports': ['global'],
            'historical': 's26',
        },
        '2010': {
            'name': 's26',
            'title': 'Internet, Twitter - Topics in stories where women are central to the news',
            'desc': 'Internet, Twitter - Topics in stories where women are central to the news',
            'reports': ['global'],
        },
    },
    'ws_s27': {
        '2015': {
            'name': 's27',
            'title': 'Internet, Twitter - Stories that clearly challenge stereotypes',
            'desc': 'Internet, Twitter - Stories that clearly challenge stereotypes',
            'reports': ['global'],
            'historical': 's27',
        },
        '2010': {
            'name': 's27',
            'title': 'Internet, Twitter - Stories that clearly challenge stereotypes',
            'desc': 'Internet, Twitter - Stories that clearly challenge stereotypes',
            'reports': ['global'],
        },
    },
    'ws_s28': {
        '2015': {
            'name': 's28',
            'title': 'Response to Question (z) is this story related to Covid & response to sex of person in the news',
            'desc': 'News subjects in stories related to Covid19, by sex',
            'reports': ['global'],
        },
    },
    'ws_s29': {
        '2015': {
            'name': 's29',
            'title': 'Response to Question (z) is this story related to Covid & response to sex of reporter',
            'desc': 'Reporters in stories related to Covid19, by sex',
            'reports': ['global'],
        },
    },
    'ws_sr01': {
        '2015': {
            'name': 'sr01',
            'title': 'Sex of presenters, reporters and news subjects by region',
            'desc': 'Sex of presenters, reporters and news subjects by region',
            'reports': ['global'],
            'historical': 'rs01',
        },
        '2010': {
            'name': 'sr01',
            'title': 'Sex of presenters, reporters and news subjects by region',
            'desc': 'Sex of presenters, reporters and news subjects by region',
            'reports': ['global'],
        },
    },
    'ws_sr02': {
        '2015': {
            'name': 'sr02',
            'title': 'News subjects in main topic areas by region',
            'desc': 'News subjects in main topic areas by region',
            'reports': ['global'],
            'historical': 'sr02',
        },
        '2010': {
            'name': 'sr02',
            'title': 'News subjects in main topic areas by region',
            'desc': 'News subjects in main topic areas by region',
            'reports': ['global'],
        },
    },
    'ws_sr03': {
        '2015': {
            'name': 'sr03',
            'title': 'Function of news subjects by region',
            'desc': 'Function of news subjects by region',
            'reports': ['global'],
            'historical': 'sr03',
        },
        '2010': {
            'name': 'sr03',
            'title': 'Function of news subjects by region',
            'desc': 'Function of news subjects by region',
            'reports': ['global'],
        },
    },
    'ws_sr04': {
        '2015': {
            'name': 'sr04',
            'title': 'Print only - News subjects in photographs by region',
            'desc': 'Print only - News subjects in photographs by region',
            'reports': ['global'],
            'historical': 'sr04',
        },
        '2010': {
            'name': 'sr04',
            'title': 'Print only - News subjects in photographs by region',
            'desc': 'Print only - News subjects in photographs by region',
            'reports': ['global'],
        },
    },
    'ws_sr05': {
        '2015': {
            'name': 'sr05',
            'title': 'Presenters and reporters, by region, by medium',
            'desc': '',
            'reports': ['global'],
            'historical': 'sr05',
        },
        '2010': {
            'name': 'sr05',
            'title': 'Presenters and reporters, by region, by medium',
            'desc': 'Presenters and reporters, by region, by medium',
            'reports': ['global'],
        },
    },
    'ws_sr06': {
        '2015': {
            'name': 'sr06',
            'title': 'Reporters in major topic areas, by region',
            'desc': 'Reporters in major topic areas, by region',
            'reports': ['global'],
            'historical': 'sr06',
        },
        '2010': {
            'name': 'sr06',
            'title': 'Reporters in major topic areas, by region',
            'desc': 'Reporters in major topic areas, by region',
            'reports': ['global'],
        }
    },
    'ws_sr07': {
        '2015': {
            'name': 'sr07',
            'title': 'Reporters and sex of news subject, by region',
            'desc': 'Reporters and sex of news subject, by region',
            'reports': ['global'],
            'historical': 'sr07',
        },
        '2010': {
            'name': 'sr07',
            'title': 'Reporters and sex of news subject, by region',
            'desc': 'Reporters and sex of news subject, by region',
            'reports': ['global'],
        },
    },
    'ws_sr08': {
        '2015': {
            'name': 'sr08',
            'title': 'Stories where women are central to the news, by region',
            'desc': 'Stories where women are central to the news, by region',
            'reports': ['global'],
            'historical': 'sr08',
        },
        '2010': {
            'name': 'sr08',
            'title': 'Stories where women are central to the news, by region',
            'desc': 'Stories where women are central to the news, by region',
            'reports': ['global'],
        }
    },
    'ws_sr09': {
        '2015': {
            'name': 'sr09',
            'title': 'Stories where issues of gender (in)equality are raised, by region',
            'desc': 'Stories where issues of gender (in)equality are raised, by region',
            'reports': ['global'],
            'historical': 'sr09',
        },
        '2010': {
            'name': 'sr09',
            'title': 'Stories where issues of gender (in)equality are raised, by region',
            'desc': 'Stories where issues of gender (in)equality are raised, by region',
            'reports': ['global'],
        },
    },
    'ws_sr10': {
        '2015': {
            'name': 'sr10',
            'title': 'Stories that clearly challenge gender stereotypes, by region',
            'desc': 'Stories that clearly challenge gender stereotypes, by region',
            'reports': ['global'],
            'historical': 'sr10'
        },
        '2010': {
            'name': 'sr10',
            'title': 'Stories that clearly challenge gender stereotypes, by region',
            'desc': 'Stories that clearly challenge gender stereotypes, by region',
            'reports': ['global'],
        },
    },
}


REGION_COUNTRY_MAP = {
    'Africa': [
        'BJ', 'BW', 'BF', 'BI', 'CM', 'CV', 'CF', 'TD', 'KM', 'CD', 'CG', 'GQ',
        'ET', 'GA', 'GM', 'GH', 'GW', 'GN', 'CI', 'KE', 'LS', 'LR', 'MG', 'MW',
        'ML', 'MR', 'MU', 'NA', 'NE', 'NG', 'SN', 'SL', 'SO', 'ZA', 'SD', 'SS',
        'SZ', 'TZ', 'TG', 'UG', 'ZM', 'ZW', 'SC'],
    'Asia': [
        'AF', 'BD', 'BT', 'CN', 'IN', 'ID', 'JP', 'KG', 'MY', 'MN', 'NP', 'PK', 'PH',
        'KR', 'TW', 'VU', 'VN', 'MO', 'HK', 'MM', 'KH'],
    'Caribbean': [
        'AG', 'BS', 'BB', 'BZ', 'CU', 'DO', 'DM', 'GD', 'GY', 'HT', 'JM', 'KY',
        'LC', 'VC', 'SR', 'TT', 'PR'],
    'Europe': [
        'AL', 'AM', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'DK', 'EE', 'FI', 'FR',
        'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'KZ', 'LU', 'MK', 'MT', 'MD',
        'ME', 'NL', 'NO', 'PL', 'PT', 'RO', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH',
        'TR', 'GB', 'QM', 'QN', 'QO', 'QP', 'QQ', 'QR', 'WL', 'SQ', 'EN', 'CY',
        'RU', 'GL'],
    'Latin America': [
        'AR', 'BO', 'BR', 'CL', 'CO', 'CR', 'EC', 'GT', 'HN', 'MX', 'NI', 'PE',
        'PY', 'SV', 'UY', 'VE'],
    'Middle East': [
        'EG', 'IL', 'IQ', 'LB', 'MA', 'PS', 'TN', 'JO'],
    'North America': [
        'CA', 'US'],
    'Pacific Islands': [
        'AU', 'FJ', 'NZ', 'WS', 'SB', 'TO', 'PG'],
    'Transnational': [
        'XI'],
}


GROUP_TOPICS_MAP = OrderedDict([
    ('1', [1, 2, 3, 4, 5, 6, 7]),
    ('2', [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]),
    ('3', [19, 20, 21, 22, 23, 24, 25, 26, 27]),
    ('4', [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]),
    ('5', [42, 43, 44, 45, 46, 47]),
    ('6', [48, 49, 50]),
    ('7', [51, 52, 53, 54, 55, 56, 57]),
    ('8', [58])
])

TOPIC_GROUPS = {
    1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1,
    8: 2, 9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 2,
    19: 3, 20: 3, 21: 3, 22: 3, 23: 3, 24: 3, 25: 3, 26: 3, 27: 3,
    28: 4, 29: 4, 30: 4, 31: 4, 32: 4, 33: 4, 34: 4, 35: 4, 36: 4, 37: 4, 38: 4, 39: 4, 40: 4, 41: 4,
    42: 5, 43: 5, 44: 5, 45: 5, 46: 5, 47: 5,
    48: 6, 49: 6, 50: 6,
    51: 7, 52: 7, 53: 7, 54: 7, 55: 7, 56: 7, 57: 7,
    58: 8
}

MAJOR_TOPICS = (
    (1, 'Politics and Government'),
    (2, 'Economy'),
    (3, 'Science and Health'),
    (4, 'Social and Legal'),
    (5, 'Crime and Violence'),
    (6, 'Gender & Related'),
    (7, 'Celebrity, Arts and Media, Sports'),
    (8, 'Other')
)

# Topic recodes for women focus areas
FOCUS_TOPICS = (
    (1, 'Political participation'),
    (2, 'Peace and security'),
    (3, 'Economic participation'),
)

FOCUS_TOPIC_IDS = {
    1: [1],
    2: [2, 5, 6, 44, 45, 47],
    3: [11, 13],
}

FOCUS_TOPIC_ID_MAP = {x: ft for ft, topics in FOCUS_TOPIC_IDS.items() for x in topics}

FORMATS = {
    'heading': {
        'font_name': 'Arial',
        'bold': True,
        'font_size': '10'
    },

    'col_heading': {
        'font_name': 'Arial',
        'font_size': '10',
        'align': 'center',
        'bg_color': '#99CCFF',
        'border': 1
    },
    'col_heading_def': {
        'font_name': 'Arial',
        'font_size': '10',
        'align': 'center',
        'bg_color': '#99CCFF'
    },
    'sec_col_heading': {
        'font_name': 'Arial',
        'font_size': '10',
        'align': 'center',
        'bg_color': '#CCFFFF',
        'border': 1
    },
    'sec_col_heading_def': {
        'font_name': 'Arial',
        'font_size': '10',
        'align': 'center',
        'bg_color': '#CCFFFF'
    },
    'label': {
        'font_name': 'Arial',
        'font_size': '10'
    },
    'N': {
        'font_name': 'Arial',
        'font_size': '10',
        'font_color': '#3737FF',
    },
    'P': {
        'font_name': 'Arial',
        'font_size': '10',
        'font_color': '#3737FF',
        'num_format': 9
    }
}

REPORTER_MEDIA = [
    'Radio',
    'Television'
]

SPECIAL_QUESTIONS = OrderedDict([
    ("special_qn_1", "Special Question 1"),
    ("special_qn_2", "Special Question 2"),
    ("special_qn_3", "Special Question 3"),
])
