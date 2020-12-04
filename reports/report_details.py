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
    return [(code, name) for code, name in list(countries) if code in captured_country_codes]


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
        'name': '1',
        'title': 'Participating Countries',
        'desc': 'Breakdown of all media by region',
        'reports': ['global'],
        'historical': '1',
    },
    'ws_02': {
        'name': '2',
        'title': 'Participating Countries in each Region',
        'desc': 'Breakdown of all media by country',
        'reports': ['global', 'region'],
        'historical': '2',
    },
    'ws_03': {
        'name': '3',
        'title': 'Counts of media monitored',
        'desc': 'Total number of distinct media monitored',
        'reports': ['global'],
        'historical': '3',
    },
    'ws_04': {
        'name': '4',
        'title': 'Topics in the news by region',
        'desc': 'Breakdown of major news topics by region by medium',
        'reports': ['global', 'region'],
        'historical': '4',
    },
    'ws_05': {
        'name': '5',
        'title': 'Summary of women in the news, by GMMP year',
        'desc': 'Overall presence of women in news',
        'reports': ['global', 'region', 'country'],
        'historical': '5',
    },
    'ws_06': {
        'name': '6',
        'title': 'Breakdown of women in the news in major topics by region',
        'desc': 'Women in the news (sources) in major news topics by region ',
        'reports': ['global', 'region'],
        'historical': '6',
    },
    'ws_07': {
        'name': '7',
        'title': 'Women in the news (sources) by medium',
        'desc': 'Breakdown by sex of all mediums',
        'reports': ['global', 'region', 'country'],
        'historical': '7',
    },
    'ws_08': {
        'name': '8',
        'title': 'Sex of news subjects (sources) inlocal,national,sub-regional/regional, foreign/intnl news',
        'desc': 'Breakdown by sex local,national,sub-regional/regional, intnl news',
        'reports': ['global', 'region', 'country'],
        'historical': '8',
    },
    'ws_09': {
        'name': '9',
        'title': 'Sex of news subjects in different story topics',
        'desc': 'Breakdown of topic by sex',
        'reports': ['global', 'region'],
        'historical': '9',
    },
    'ws_10': {
        'name': '10',
        'title': 'Space allocated to major topics in Newspapers',
        'desc': 'Breakdown by major topic by space (q.4) in newspapers',
        'reports': ['global', 'region', 'country'],
        'historical': '10',
    },
    'ws_11': {
        'name': '11',
        'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by major topic',
        'desc': 'Breakdown by major topic by reference to gender equality/human rights/policy',
        'reports': ['global', 'region', 'country'],
        'historical': '11',
    },
    'ws_12': {
        'name': '12',
        'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by region',
        'desc': 'Breakdown by major topic by region by reference to gender equality/human rights/policy',
        'reports': ['global', 'region'],
        'historical': '12',
    },
    'ws_13': {
        'name': '13',
        'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by sex of reporter',
        'desc': 'B.down by major topic by sex of reporter by reference to gender equality/human rights/policy',
        'reports': ['global', 'region',  'country'],
        'historical': '13',
    },
    'ws_14': {
        'name': '14',
        'title': 'Position or occupation of news sources, by sex',
        'desc': 'Breakdown of new sources by occupation and sex',
        'reports': ['global', 'region', 'country'],
        'historical': '14',
    },
    'ws_15': {
        'name': '15',
        'title': 'News subject''s Function in news story, by sex',
        'desc': 'Breakdown by sex and function',
        'reports': ['global', 'region', 'country'],
        'historical': '15',
    },
    'ws_16': {
        'name': '16',
        'title': 'Function of news subjects by sex - by occupation',
        'desc': 'Breakdown of  Function of news subjects by sex - by occupation',
        'reports': ['global', 'region', 'country'],
        'historical': '16',
    },
    'ws_17': {
        'name': '17',
        'title': 'Function of news subjects by sex - by age',
        'desc': 'Breakdown of  Function of news subjects by sex - by age',
        'reports': ['global', 'region', 'country'],
        'historical': '17',
    },
    'ws_18': {
        'name': '18',
        'title': 'Age of news subjects by print, by sex',
        'desc': 'B.down of  Age of news subjects by print, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '18',
    },
    'ws_19': {
        'name': '19',
        'title': 'Age of Television news subjects, by sex',
        'desc': 'B.down of  Age of Television news subjects, by sex (age captured for Television only)',
        'reports': ['global', 'region', 'country'],
        'historical': '19',
    },
    'ws_20': {
        'name': '20',
        'title': 'Functions and Occupations by sex of news subject',
        'desc': 'B.down of  news subjects\' functions and occupations by sex of news subject',
        'reports': ['global', 'region', 'country'],
        'historical': '20',
    },
    'ws_21': {
        'name': '21',
        'title': 'Breakdown by victim type by sex',
        'desc': 'News Subjects who are portrayed as victims, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '21',
    },
    'ws_23': {
        'name': '23',
        'title': 'Breakdown by survivor type by sex',
        'desc': 'News subjects who are portrayed as survivors, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '23',
    },
    'ws_24': {
        'name': '24',
        'title': 'Breakdown by family status, by sex.',
        'desc': 'News subjects who are identified by family status, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '24',
    },
    'ws_25': {
        'name': '25',
        'title': 'B.down by sex of subject, family status, by sex of reporter',
        'desc': 'News subjects who are identified by family status, by sex of news subject, by sex of reporter',
        'reports': ['global', 'region', 'country'],
        'historical': '25',
    },
    'ws_26': {
        'name': '26',
        'title': 'Breakdown of  news subjects quoted, by sex',
        'desc': 'News subjects quoted, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '26',
    },
    'ws_27': {
        'name': '27',
        'title': 'Breakdown of News subjects photographed, by sex',
        'desc': 'News subjects photographed, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '27',
    },
    'ws_28': {
        'name': '28',
        'title': 'Breakdown of total female reporters & presenters by region by medium ',
        'desc': 'Female reporters, announcers and presenters all media, by region',
        'reports': ['global', 'region', 'country'],
        'historical': '28',
    },
    'ws_29': {
        'name': '29',
        'title': 'Breakdown of female reporters in domestic & foreign stories, by region',
        'desc': 'Reporters in domestic & foreign stories (scope) , by region, by sex of reporter region',
        'reports': ['global', 'region', 'country'],
        'historical': '29',
    },
    'ws_30': {
        'name': '30',
        'title': 'Breakdown of female reporters, by major topic, by region',
        'desc': 'Reporters, by sex on major topics, by region',
        'reports': ['global', 'region', 'country'],
        'historical': '30',
    },
    'ws_31': {
        'name': '31',
        'title': 'Breakdown of Reporters, by sex on different topics - Detail',
        'desc': 'Reporters, by sex on different topics - Detail',
        'reports': ['global'],
        'historical': '31',
    },
    'ws_32': {
        'name': '32',
        'title': 'Topics in the news - Detail by medium for female reporters',
        'desc': 'Topics in the news - Detail by medium for female reporters',
        'reports': ['global'],
        'historical': '32',
    },
    'ws_34': {
        'name': '34',
        'title': 'Breakdown of News Subject (sex of source) selection by female & male reporters',
        'desc': 'Selection of News Subject (sex of source, in rows) by female & male reporters (in columns)',
        'reports': ['global', 'region', 'country'],
        'historical': '34',
    },
    'ws_35': {
        'name': '35',
        'title': 'Breakdown of television Announcers & Reporters, by age, by sex',
        'desc': 'Age of television Announcers & Reporters, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '35',
    },
    'ws_36': {
        'name': '36',
        'title': 'Breakdown of Stories with Women as central focus (is this story about a particular woman or women) by sex of reporter',
        'desc': 'Stories with Women as central focus  by sex of reporter',
        'reports': ['global', 'region', 'country'],
        'historical': '36',
    },
    'ws_38': {
        'name': '38',
        'title': 'Breakdown of Stories with Women as a central Focus by major topic',
        'desc': 'Stories with Women as a central Focus by major topic',
        'reports': ['global', 'region', 'country'],
        'historical': '38',
    },
    'ws_39': {
        'name': '39',
        'title': 'Breakdown of Stories with Women as a central Focus by minor topic',
        'desc': 'Stories with Women as a central Focus by minor topic',
        'reports': ['global'],
        'historical': '39',
    },
    'ws_40': {
        'name': '40',
        'title': 'Breakdown of Stories with Women as a central Focus by topic and region',
        'desc': 'Stories with Women as a central Focus by topic and region',
        'reports': ['global'],
        'historical': '40',
    },
    'ws_41': {
        'name': '41',
        'title': 'Breakdown of Stories where issues of gender equality/inequality are raised by topic',
        'desc': 'Stories where issues of gender equality/inequality are raised by topic',
        'reports': ['global', 'region', 'country'],
        'historical': '41',
    },
    'ws_42': {
        'name': '42',
        'title': 'Breakdown of Stories where issues of gender equality/inequality are raised by region',
        'desc': 'Stories where issues of gender equality/inequality are raised by region',
        'reports': ['global'],
        'historical': '42',
    },
    'ws_43': {
        'name': '43',
        'title': 'Breakdown of Stories where issues of gender equality/inequality are raised by sex of reporter',
        'desc': 'Stories where issues of gender equality/inequality are raised by sex of reporter',
        'reports': ['global', 'region', 'country'],
        'historical': '43',
    },
    'ws_44': {
        'name': '44',
        'title': 'Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
        'desc': 'Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
        'reports': ['global', 'region'],
        'historical': '44',
    },
    'ws_45': {
        'name': '45',
        'title': 'Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
        'desc': 'Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
        'reports': ['global', 'region'],
        'historical': '45',
    },
    'ws_46': {
        'name': '46',
        'title': 'Story clearly challenges gender stereotypes by region by major news topic',
        'desc': 'Stories where stereotypes are challenged/ supported by news topic',
        'reports': ['global'],
        'historical': '46',
    },
    'ws_47': {
        'name': '47',
        'title': 'Story clearly challenges gender stereotypes by major topic',
        'desc': 'Stories where stereotypes are challenged/ supported by topic',
        'reports': ['global', 'region', 'country'],
        'historical': '47',
    },
    'ws_48': {
        'name': '48',
        'title': 'Story clearly challenges gender stereotypes by sex of rep',
        'desc': 'Stories where stereotypes are challenged/ supported by gender of rep',
        'reports': ['global', 'region', 'country'],
        'historical': '48',
    },
    'ws_49': {
        'name': '49',
        'title': 'Internet - Main topics by region',
        'desc': 'Internet - Main topics by region',
        'reports': ['global', 'region', 'country'],
        'historical': '49',
    },
    'ws_50': {
        'name': '50',
        'title': 'Internet - Story shared on Twitter',
        'desc': 'Internet - Story shared on Twitter',
        'reports': ['global', 'country'],
        'historical': '50',
    },
    'ws_51': {
        'name': '51',
        'title': 'Internet - Story shared on Facebook',
        'desc': 'Internet - Story shared on Facebook',
        'reports': ['global', 'country'],
        'historical': '51',
    },
    'ws_52': {
        'name': '52',
        'title': 'Internet - Reference to gender equality/HR policies',
        'desc': 'Internet - Reference to gender equality/HR policies',
        'reports': ['global', 'country'],
        'historical': '52',
    },
    'ws_53': {
        'name': '53',
        'title': 'Internet - Female reporters in main stories',
        'desc': 'Internet - Female reporters in main stories',
        'reports': ['global', 'region', 'country'],
        'historical': '53',
    },
    'ws_54': {
        'name': '54',
        'title': 'Internet - Overall presence of women',
        'desc': 'Internet - Overall presence of women',
        'reports': ['global', 'region', 'country'],
        'historical': '54',
    },
    'ws_55': {
        'name': '55',
        'title': 'Internet - Occupation of Female news subjects',
        'desc': 'Internet - Occupation of Female news subjects',
        'reports': ['global'],
        'historical': '55',
    },
    'ws_56': {
        'name': '56',
        'title': 'Internet - Functions of news subjects',
        'desc': 'Internet - Functions of news subjects',
        'reports': ['global', 'region', 'country'],
        'historical': '56',
    },
    'ws_57': {
        'name': '57',
        'title': 'Internet - News subjects who are identified by family status',
        'desc': 'Internet - News subjects who are identified by family status',
        'reports': ['global', 'country'],
        'historical': '57',
    },
    'ws_58': {
        'name': '58',
        'title': 'Internet - News subjects in multimedia web components',
        'desc': 'Internet - News subjects in multimedia web components',
        'reports': ['global', 'country'],
        'historical': '58',
    },
    'ws_59': {
        'name': '59',
        'title': 'Internet - Selection of News Subjects',
        'desc': 'Internet - Selection of News Subjects by sex of reporter (columns) and sex of subject (rows)',
        'reports': ['global', 'country'],
        'historical': '59',
    },
    'ws_60': {
        'name': '60',
        'title': 'Internet - Age of news subjects',
        'desc': 'Internet - Age of news subjects',
        'reports': ['global', 'country'],
        'historical': '60',
    },
    'ws_61': {
        'name': '61',
        'title': 'Internet - News subjects who are directly quoted',
        'desc': 'Internet - News subjects who are directly quoted',
        'reports': ['global', 'country'],
        'historical': '61',
    },
    'ws_62': {
        'name': '62',
        'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'desc': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'reports': ['global', 'region', 'country'],
        'historical': '62',
    },
    'ws_63': {
        'name': '63',
        'title': 'Internet -Stories where stereotypes are clearly challenged',
        'desc': 'Internet -Stories where stereotypes are clearly challenged',
        'reports': ['global', 'region', 'country'],
        'historical': '63',
    },
    'ws_64': {
        'name': '64',
        'title': 'Internet -Stories with Women as a central Focus',
        'desc': 'Internet -Stories with Women as a central Focus',
        'reports': ['global', 'region', 'country'],
        'historical': '64',
    },
    'ws_65': {
        'name': '65',
        'title': 'Twitter - Original tweet or retweet',
        'desc': 'Twitter - Original tweet or retweet',
        'reports': ['global', 'region', 'country'],
        'historical': '65',
    },
    'ws_66': {
        'name': '66',
        'title': 'Twitter - Overall presence of women',
        'desc': 'Twitter - Overall presence of women',
        'reports': ['global', 'region', 'country'],
        'historical': '66',
    },
    'ws_67': {
        'name': '67',
        'title': 'Twitter - Female reporters & journalists',
        'desc': 'Twitter - Female reporters & journalists',
        'reports': ['global', 'region', 'country'],
        'historical': '67',
    },
    'ws_68': {
        'name': '68',
        'title': 'Twitter - Women\'s centrality',
        'desc': 'Twitter - Women\'s centrality',
        'reports': ['global', 'region', 'country'],
        'historical': '68',
    },
    'ws_68b': {
        'name': '68b',
        'title': 'Twitter - Challenging Stereotypes',
        'desc': 'Twitter - Challenging Stereotypes',
        'reports': ['global', 'region', 'country'],
        'historical': '68b',
    },
    'ws_70': {
        'name': '70',
        'title': 'Twitter - Hashtags',
        'desc': 'Twitter - Hashtags',
        'reports': ['global'],
        'historical': '70',
    },
    'ws_71': {
        'name': '71',
        'title': 'Key themes, women\'s overall presence',
        'desc': 'Key themes, women\'s overall presence',
        'reports': ['global', 'region', 'country'],
        'historical': '71',
    },
    'ws_72': {
        'name': '72',
        'title': 'Key themes, female reporters',
        'desc': 'Key themes, female reporters',
        'reports': ['global', 'region', 'country'],
        'historical': '72',
    },
    'ws_73': {
        'name': '73',
        'title': 'Key themes, selection of sources by sex of reporter',
        'desc': 'Key themes, selection of sources by sex of reporter',
        'reports': ['global', 'region', 'country'],
        'historical': '73',
    },
    'ws_74': {
        'name': '74',
        'title': 'Key themes, women\'s centrality',
        'desc': 'Stories with Women as a central focus, by women centrality topic',
        'reports': ['global', 'region', 'country'],
        'historical': '74',
    },
    'ws_75': {
        'name': '75',
        'title': 'Key themes, challenging stereotypes',
        'desc': 'Key themes, challenging stereotypes',
        'reports': ['global', 'region', 'country'],
        'historical': '75',
    },
    'ws_76': {
        'name': '76',
        'title': 'Key themes, reference to gender equality/HR policies',
        'desc': 'Key themes, reference to gender equality/HR policies',
        'reports': ['global', 'region', 'country'],
        'historical': '76',
    },
    'ws_77': {
        'name': '77',
        'title': 'Key themes, portrayal as victims',
        'desc': 'Key themes, portrayal as victims',
        'reports': ['global', 'region', 'country'],
        'historical': '77',
    },
    'ws_78': {
        'name': '78',
        'title': 'Key themes, portrayal as survivors',
        'desc': 'Key themes, portrayal as survivors',
        'reports': ['global', 'region', 'country'],
        'historical': '78',
    },
    'ws_79': {
        'name': '79',
        'title': 'Internet - Main topics by region',
        'desc': 'Internet - Main topics by region',
        'reports': ['global'],
        'historical': '79',
    },
    'ws_80': {
        'name': '80',
        'title': 'Internet - Story shared on Twitter',
        'desc': 'Internet - Story shared on Twitter',
        'reports': ['global'],
        'historical': '80',
    },
    'ws_81': {
        'name': '81',
        'title': 'Internet - Story shared on Facebook',
        'desc': 'Internet - Story shared on Facebook',
        'reports': ['global'],
        'historical': '81',
    },
    'ws_82': {
        'name': '82',
        'title': 'Internet - Reference to gender equality/HR policies',
        'desc': 'Internet - Reference to gender equality/HR policies',
        'reports': ['global'],
        'historical': '82',
    },
    'ws_83': {
        'name': '83',
        'title': 'Internet - reporters in main stories',
        'desc': 'Internet - reporters in main stories',
        'reports': ['global'],
        'historical': '83',
    },
    'ws_84': {
        'name': '84',
        'title': 'Internet - Occupation of Female news subjects',
        'desc': 'Internet - Occupation of Female news subjects',
        'reports': ['global'],
        'historical': '84',
    },
    'ws_85': {
        'name': '85',
        'title': 'Internet - Functions of news subjects',
        'desc': 'Internet - Functions of news subjects',
        'reports': ['global'],
        'historical': '85',
    },
    'ws_86': {
        'name': '86',
        'title': 'Internet - News subjects who are identified by family status',
        'desc': 'Internet - News subjects who are identified by family status',
        'reports': ['global'],
        'historical': '86',
    },
    'ws_87': {
        'name': '87',
        'title': 'Internet - News subjects in multimedia web components',
        'desc': 'Internet - News subjects in multimedia web components',
        'reports': ['global'],
        'historical': '87',
    },
    'ws_88': {
        'name': '88',
        'title': 'Internet - Selection of News Subjects',
        'desc': 'Internet - Selection of News Subjects',
        'reports': ['global'],
        'historical': '88',
    },
    'ws_89': {
        'name': '89',
        'title': 'Internet - Age of news subjects',
        'desc': 'Internet - Age of news subjects',
        'reports': ['global'],
        'historical': '89',
    },
    'ws_90': {
        'name': '90',
        'title': 'Internet - News subjects who are directly quoted',
        'desc': 'Internet - News subjects who are directly quoted',
        'reports': ['global'],
        'historical': '90',
    },
    'ws_91': {
        'name': '91',
        'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'desc': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'reports': ['global'],
        'historical': '91',
    },
    'ws_92': {
        'name': '92',
        'title': 'Internet -Stories where stereotypes are clearly challenged',
        'desc': 'Internet -Stories where stereotypes are clearly challenged',
        'reports': ['global'],
        'historical': '92',
    },
    'ws_93': {
        'name': '93',
        'title': 'Internet -Stories with Women as a central Focus',
        'desc': 'Internet -Stories with Women as a central Focus',
        'reports': ['global'],
        'historical': '93',
    },
    'ws_94': {
        'name': '94',
        'title': 'Twitter - Original tweet or retweet',
        'desc': 'Twitter - Original tweet or retweet',
        'reports': ['global'],
        'historical': '94',
    },
    'ws_95': {
        'name': '95',
        'title': 'Twitter - Female reporters',
        'desc': 'Twitter - Female reporters',
        'reports': ['global'],
        'historical': '95',
    },
    'ws_96': {
        'name': '96',
        'title': 'Twitter - Women\'s centrality',
        'desc': 'Twitter - Women\'s centrality',
        'reports': ['global'],
        'historical': '96',
    },
    'ws_97': {
        'name': '97',
        'title': 'Twitter - Challenging Stereotypes',
        'desc': 'Twitter - Challenging Stereotypes',
        'reports': ['global'],
        'historical': '97',
    },
    'ws_s01': {
        'name': 's01',
        'title': 'Sex of presenters, reporters and news subjects',
        'desc': 'Sex of presenters, reporters and news subjects',
        'reports': ['global'],
        'historical': 's01',
    },
    'ws_s02': {
        'name': 's02',
        'title': 'News subjects in television, radio and newspapers',
        'desc': 'News subjects in television, radio and newspapers',
        'reports': ['global'],
        'historical': 's02',
    },
    'ws_s03': {
        'name': 's03',
        'title': 'News subjects in major topic areas',
        'desc': 'News subjects in major topic areas',
        'reports': ['global'],
        'historical': 's03',
    },
    'ws_s04': {
        'name': 's04',
        'title': 'News subjects in major occupational groups',
        'desc': 'News subjects in major occupational groups',
        'reports': ['global'],
        'historical': 's04',
    },
    'ws_s05': {
        'name': 's05',
        'title': 'Function of news subjects',
        'desc': 'Function of news subjects',
        'reports': ['global'],
        'historical': 's05',
    },
    'ws_s06': {
        'name': 's06',
        'title': 'News subjects who are victims',
        'desc': 'News subjects who are victims',
        'reports': ['global'],
        'historical': 's06',
    },
    'ws_s07': {
        'name': 's07',
        'title': 'News subjects mentioned by family status',
        'desc': 'News subjects mentioned by family status',
        'reports': ['global'],
        'historical': 's07',
    },
    'ws_s08': {
        'name': 's08',
        'title': 'News subjects quoted in newspapers',
        'desc': 'News subjects quoted in newspapers',
        'reports': ['global'],
        'historical': 's08',
    },
    'ws_s09': {
        'name': 's09',
        'title': 'Print only - News subjects appearing in newspaper photographs',
        'desc': 'Print only - News subjects appearing in newspaper photographs',
        'reports': ['global'],
        'historical': 's09',
    },
    'ws_s10': {
        'name': 's10',
        'title': 'Presenters and reporters in television, radio and newspapers',
        'desc': 'Presenters and reporters in television, radio and newspapers',
        'reports': ['global'],
        'historical': 's10',
    },
    'ws_s11': {
        'name': 's11',
        'title': 'Reporters in major topic areas',
        'desc': 'Reporters in major topic areas',
        'reports': ['global'],
        'historical': 's11',
    },
    'ws_s12': {
        'name': 's12',
        'title': 'Topics in stories where women are central to the news',
        'desc': 'Topics in stories where women are central to the news',
        'reports': ['global'],
        'historical': 's12',
    },
    'ws_s13': {
        'name': 's13',
        'title': 'Sex of reporter in stories with female and male news subjects',
        'desc': 'Sex of reporter in stories with female and male news subjects',
        'reports': ['global'],
        'historical': 's13',
    },
    'ws_s14': {
        'name': 's14',
        'title': 'Stories that clearly challenge stereotypes',
        'desc': 'Stories that clearly challenge stereotypes',
        'reports': ['global'],
        'historical': 's14',
    },
    'ws_s15': {
        'name': 's15',
        'title': 'Stories that highlight gender equality or inequality',
        'desc': 'Stories that highlight gender equality or inequality',
        'reports': ['global'],
        'historical': 's15',
    },
    'ws_s16': {
        'name': 's16',
        'title': 'Stories that mention human rights or equality legislation and policies',
        'desc': 'Stories that mention human rights or equality legislation and policies',
        'reports': ['global'],
        'historical': 's16',
    },
    'ws_s17': {
        'name': 's17',
        'title': 'Internet, Twitter - Sex of reporters and news subjects',
        'desc': 'Internet, Twitter - Sex of reporters and news subjects',
        'reports': ['global'],
        'historical': 's17',
    },
    'ws_s18': {
        'name': 's18',
        'title': 'Internet, Twitter - News subjects on Internet and Twitter news',
        'desc': 'Internet, Twitter - News subjects on Internet and Twitter news',
        'reports': ['global'],
        'historical': 's18',
    },
    'ws_s19': {
        'name': 's19',
        'title': 'Internet, Twitter - News subjects in major topic areas',
        'desc': 'Internet, Twitter - News subjects in major topic areas',
        'reports': ['global'],
        'historical': 's19',
    },
    'ws_s20': {
        'name': 's20',
        'title': 'Internet - News subjects in major occupational groups',
        'desc': 'Internet - News subjects in major occupational groups',
        'reports': ['global'],
        'historical': 's20',
    },
    'ws_s21': {
        'name': 's21',
        'title': 'Internet - Function of news subjects',
        'desc': 'Internet - Function of news subjects',
        'reports': ['global'],
        'historical': 's21',
    },
    'ws_s22': {
        'name': 's22',
        'title': 'Internet - News subjects who are victims',
        'desc': 'Internet - News subjects who are victims',
        'reports': ['global'],
        'historical': 's22',
    },
    'ws_s23': {
        'name': 's23',
        'title': 'Internet - News subjects quoted',
        'desc': 'Internet - News subjects quoted',
        'reports': ['global'],
        'historical': 's23',
    },
    'ws_s24': {
        'name': 's24',
        'title': 'Internet, Twitter - News subjects appearing in images and video plug-ins',
        'desc': 'Internet, Twitter - News subjects appearing in images and video plug-ins',
        'reports': ['global'],
        'historical': 's24',
    },
    'ws_s25': {
        'name': 's25',
        'title': 'Internet, Twitter - Reporters in major topic areas',
        'desc': 'Internet, Twitter - Reporters in major topic areas',
        'reports': ['global'],
        'historical': 's25',
    },
    'ws_s26': {
        'name': 's26',
        'title': 'Internet, Twitter - Topics in stories where women are central to the news',
        'desc': 'Internet, Twitter - Topics in stories where women are central to the news',
        'reports': ['global'],
        'historical': 's26',
    },
    'ws_s27': {
        'name': 's27',
        'title': 'Internet, Twitter - Stories that clearly challenge stereotypes',
        'desc': 'Internet, Twitter - Stories that clearly challenge stereotypes',
        'reports': ['global'],
        'historical': 's27',
    },
    'ws_sr01': {
        'name': 'rs01',
        'title': 'Sex of presenters, reporters and news subjects by region',
        'desc': 'Sex of presenters, reporters and news subjects by region',
        'reports': ['global'],
        'historical': 'rs01',
    },
    'ws_sr02': {
        'name': 'sr02',
        'title': 'News subjects in main topic areas by region',
        'desc': 'News subjects in main topic areas by region',
        'reports': ['global'],
        'historical': 'sr02',
    },
    'ws_sr03': {
        'name': 'sr03',
        'title': 'Function of news subjects by region',
        'desc': 'Function of news subjects by region',
        'reports': ['global'],
        'historical': 'sr03',
    },
    'ws_sr04': {
        'name': 'sr04',
        'title': 'Print only - News subjects in photographs by region',
        'desc': 'Print only - News subjects in photographs by region',
        'reports': ['global'],
        'historical': 'sr04',
    },
    'ws_sr05': {
        'name': 'sr05',
        'title': 'Presenters and reporters, by region, by medium',
        'desc': 'Presenters and reporters, by region, by medium',
        'reports': ['global'],
        'historical': 'sr05',
    },
    'ws_sr06': {
        'name': 'sr06',
        'title': 'Reporters in major topic areas, by region',
        'desc': 'Reporters in major topic areas, by region',
        'reports': ['global'],
        'historical': 'sr06',
    },
    'ws_sr07': {
        'name': 'sr07',
        'title': 'Reporters and sex of news subject, by region',
        'desc': 'Reporters and sex of news subject, by region',
        'reports': ['global'],
        'historical': 'sr07',
    },
    'ws_sr08': {
        'name': 'sr08',
        'title': 'Stories where women are central to the news, by region',
        'desc': 'Stories where women are central to the news, by region',
        'reports': ['global'],
        'historical': 'sr08',
    },
    'ws_sr09': {
        'name': 'sr09',
        'title': 'Stories where issues of gender (in)equality are raised, by region',
        'desc': 'Stories where issues of gender (in)equality are raised, by region',
        'reports': ['global'],
        'historical': 'sr09',
    },
    'ws_sr10': {
        'name': 'sr10',
        'title': 'Stories that clearly challenge gender stereotypes, by region',
        'desc': 'Stories that clearly challenge gender stereotypes, by region',
        'reports': ['global'],
        'historical': 'sr10',
    },
}


REGION_COUNTRY_MAP = {
    'Africa': [
        'BJ', 'BW', 'BF', 'BI', 'CM', 'CV', 'CF', 'TD', 'KM', 'CD', 'CG', 'GQ',
        'ET', 'GA', 'GM', 'GH', 'GW', 'GN', 'CI', 'KE', 'LS', 'LR', 'MG', 'MW',
        'ML', 'MR', 'MU', 'NA', 'NE', 'NG', 'SN', 'SL', 'SO', 'ZA', 'SD', 'SS',
        'SZ', 'TZ', 'TG', 'UG', 'ZM', 'ZW'],
    'Asia': [
        'AF', 'BD', 'BT', 'CN', 'IN', 'ID', 'JP', 'KG', 'MY', 'MN', 'NP', 'PK', 'PH',
        'KR', 'TW', 'VU', 'VN'],
    'Caribbean': [
        'AG', 'BS', 'BB', 'BZ', 'CU', 'DO', 'GD', 'GY', 'HT', 'JM', 'LC', 'VC',
        'SR', 'TT', 'PR'],
    'Europe': [
        'AL', 'AM', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'DK', 'EE', 'FI', 'FR',
        'GE', 'DE', 'GR', 'HU', 'IS', 'IE', 'IT', 'KZ', 'LU', 'MK', 'MT', 'MD',
        'ME', 'NL', 'NO', 'PL', 'PT', 'RO', 'RS', 'SK', 'SI', 'ES', 'SE', 'CH',
        'TR', 'GB', 'B1', 'B2', 'WL', 'SQ', 'EN', 'UK', 'CY'],
    'Latin America': [
        'AR', 'BO', 'BR', 'CL', 'CO', 'CR', 'EC', 'SV', 'GT', 'MX', 'NI', 'PY',
        'PE', 'UY', 'VE'],
    'Middle East': [
        'EG', 'IL', 'LB', 'MA', 'PS', 'TN'],
    'North America': [
        'CA', 'US'],
    'Pacific Islands': [
        'AU', 'FJ', 'NZ', 'WS', 'SB', 'TO']}


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
    48: 4, 49: 6, 50: 6,
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
