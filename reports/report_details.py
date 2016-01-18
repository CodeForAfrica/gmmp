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
    for model in sheet_models.itervalues():
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
        return [(0, [k for k, v in REGION_COUNTRY_MAP.items() if country in v][0])]


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
        'historical': '1F',
    },
    'ws_02': {
        'name': '2',
        'title': 'Participating Countries in each Region',
        'desc': 'Breakdown of all media by country',
        'reports': ['global', 'region'],
        'historical': '2F',
    },
    'ws_03': {
        'name': '3',
        'title': 'Counts of media monitored',
        'desc': 'Total number of distinct media monitored',
        'reports': ['global'],
        'historical': '2aF'
    },
    'ws_04': {
        'name': '4',
        'title': 'Topics in the news by region',
        'desc': 'Breakdown of major news topics by region by medium',
        'reports': ['global', 'region'],
        'historical': '3aF'
    },
    'ws_05': {
        'name': '5',
        'title': 'Summary of women in the news, by GMMP year',
        'desc': 'Overall presence of women in news',
        'reports': ['global', 'region', 'country'],
        'historical': '9aF',
    },
    'ws_06': {
        'name': '6',
        'title': 'Breakdown of women in the news in major topics by region',
        'desc': 'Women in the news (sources) in major news topics by region ',
        'reports': ['global', 'region'],
        'historical': '3bF',
    },
    'ws_07': {
        'name': '7',
        'title': 'Women in the news (sources) by medium',
        'desc': 'Breakdown by sex of all mediums',
        'reports': ['global', 'region', 'country'],
        'historical': '9bF'
    },
    'ws_08': {
        'name': '8',
        'title': 'Sex of news subjects (sources) inlocal,national,sub-regional/regional, foreign/intnl news',
        'desc': 'Breakdown by sex local,national,sub-regional/regional, intnl news',
        'reports': ['global', 'region', 'country'],
        'historical': '9cF'
    },
    'ws_09': {
        'name': '9',
        'title': 'Sex of news subjects in different story topics',
        'desc': 'Breakdown of topic by sex',
        'reports': ['global', 'region'],
        'historical': '9dF'
    },
    'ws_10': {
        'name': '10',
        'title': 'Space allocated to major topics in Newspapers',
        'desc': 'Breakdown by major topic by space (q.4) in newspapers',
        'reports': ['global', 'region', 'country'],
    },
    'ws_11': {
        'name': '11',
        'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by major topic',
        'desc': 'Breakdown by major topic by reference to gender equality/human rights/policy',
        'reports': ['global', 'region', 'country'],
    },
    'ws_12': {
        'name': '12',
        'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by region',
        'desc': 'Breakdown by major topic by region by reference to gender equality/human rights/policy',
        'reports': ['global', 'region'],
    },
    'ws_13': {
        'name': '13',
        'title': 'Stories making reference to issues of gender equality/inequality, legislation, policy by sex of reporter',
        'desc': 'B.down by major topic by sex of reporter by reference to gender equality/human rights/policy',
        'reports': ['global', 'region',  'country'],
    },
    'ws_14': {
        'name': '14',
        'title': 'Position or occupation of news sources, by sex',
        'desc': 'Breakdown of new sources by occupation and sex',
        'reports': ['global', 'region', 'country'],
        'historical': '9eF'
    },
    'ws_15': {
        'name': '15',
        'title': 'News subject''s Function in news story, by sex',
        'desc': 'Breakdown by sex and function',
        'reports': ['global', 'region', 'country'],
        'historical': '9fF'
    },
    'ws_16': {
        'name': '16',
        'title': 'Function of news subjects by sex - by occupation',
        'desc': 'Breakdown of  Function of news subjects by sex - by occupation',
        'reports': ['global', 'region', 'country'],
        'historical': '20aF'
    },
    'ws_17': {
        'name': '17',
        'title': 'Function of news subjects by sex - by age',
        'desc': 'Breakdown of  Function of news subjects by sex - by age',
        'reports': ['global', 'region', 'country'],
        'historical': '20bF'
    },
    'ws_18': {
        'name': '18',
        'title': 'Age of news subjects by print, by sex',
        'desc': 'B.down of  Age of news subjects by print, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '18cF'
    },
    'ws_19': {
        'name': '19',
        'title': 'Age of Television news subjects, by sex',
        'desc': 'B.down of  Age of Television news subjects, by sex (age captured for Television only)',
        'reports': ['global', 'region', 'country'],
        'historical': '18dF'
    },
    'ws_20': {
        'name': '20',
        'title': 'Functions and Occupations by sex of news subject',
        'desc': 'B.down of  news subjects\' functions and occupations by sex of news subject',
        'reports': ['global', 'region', 'country'],
        'historical': '20fF'
    },
    'ws_21': {
        'name': '21',
        'title': 'Breakdown by victim type by sex',
        'desc': 'News Subjects who are portrayed as victims, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '9gF'
    },
    'ws_23': {
        'name': '23',
        'title': 'Breakdown by survivor type by sex',
        'desc': 'News subjects who are portrayed as survivors, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '19bF'
    },
    'ws_24': {
        'name': '24',
        'title': 'Breakdown by family status, by sex.',
        'desc': 'News subjects who are identified by family status, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '9hF'
    },
    'ws_25': {
        'name': '25',
        'title': 'B.down by sex of subject, family status, by sex of reporter',
        'desc': 'News subjects who are identified by family status, by sex of news subject, by sex of reporter',
        'reports': ['global', 'region', 'country'],
        'historical': '9kF'
    },
    'ws_26': {
        'name': '26',
        'title': 'Breakdown of  news subjects quoted, by sex',
        'desc': 'News subjects quoted, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '20gF'
    },
    'ws_27': {
        'name': '27',
        'title': 'Breakdown of News subjects photographed, by sex',
        'desc': 'News subjects photographed, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '20hF'
    },
    'ws_28': {
        'name': '28',
        'title': 'Breakdown of total female reporters & presenters by region by medium ',
        'desc': 'Female reporters, announcers and presenters all media, by region',
        'reports': ['global', 'region', 'country'],
        'historical': '10bF'
    },
    'ws_29': {
        'name': '29',
        'title': 'Breakdown of female reporters in domestic & foreign stories, by region',
        'desc': 'Reporters in domestic & foreign stories (scope) , by region, by sex of reporter region',
        'reports': ['global', 'region', 'country'],
    },
    'ws_30': {
        'name': '30',
        'title': 'Breakdown of female reporters, by major topic, by region',
        'desc': 'Reporters, by sex on major topics, by region',
        'reports': ['global', 'region', 'country'],
    },
    'ws_31': {
        'name': '31',
        'title': 'Breakdown of Reporters, by sex on different topics - Detail',
        'desc': 'Rporters, by sex on different topics - Detail',
        'reports': ['global'],
        'historical': '12dF'
    },
    'ws_32': {
        'name': '32',
        'title': 'Topics in the news - Detail by medium for female reporters',
        'desc': 'Topics in the news - Detail by medium for female reporters',
        'reports': ['global'],
    },
    'ws_34': {
        'name': '34',
        'title': 'Breakdown of News Subject (sex of source) selection by female & male reporters',
        'desc': 'Selection of News Subject (sex of source, in rows) by female & male reporters (in columns)',
        'reports': ['global', 'region', 'country'],
        'historical': '13bF'
    },
    'ws_35': {
        'name': '35',
        'title': 'Breakdown of television Announcers & Reporters, by age, by sex',
        'desc': 'Age of television Announcers & Reporters, by sex',
        'reports': ['global', 'region', 'country'],
        'historical': '14F'
    },
    'ws_36': {
        'name': '36',
        'title': 'Breakdown of Stories with Women as central focus (is this story about a particular woman or women) by sex of reporter',
        'desc': 'Stories with Women as central focus  by sex of reporter',
        'reports': ['global', 'region', 'country'],
        'historical': '15aF'
    },
    'ws_38': {
        'name': '38',
        'title': 'Breakdown of Stories with Women as a central Focus by major topic',
        'desc': 'Stories with Women as a central Focus by major topic',
        'reports': ['global', 'region', 'country'],
    },
    'ws_39': {
        'name': '39',
        'title': 'Breakdown of Stories with Women as a central Focus by minor topic',
        'desc': 'Stories with Women as a central Focus by minor topic',
        'reports': ['global'],
        'historical': '15bF'
    },
    'ws_40': {
        'name': '40',
        'title': 'Breakdown of Stories with Women as a central Focus by topic and region',
        'desc': 'Stories with Women as a central Focus by topic and region',
        'reports': ['global'],
        'historical': '15cF'
    },
    'ws_41': {
        'name': '41',
        'title': 'Breakdown of Stories where issues of gender equality/inequality are raised by topic',
        'desc': 'Stories where issues of gender equality/inequality are raised by topic',
        'reports': ['global', 'region', 'country'],
        'historical': '16eF'
    },
    'ws_42': {
        'name': '42',
        'title': 'Breakdown of Stories where issues of gender equality/inequality are raised by region',
        'desc': 'Stories where issues of gender equality/inequality are raised by region',
        'reports': ['global'],
    },
    'ws_43': {
        'name': '43',
        'title': 'Breakdown of Stories where issues of gender equality/inequality are raised by sex of reporter',
        'desc': 'Stories where issues of gender equality/inequality are raised by sex of reporter',
        'reports': ['global', 'region', 'country'],
    },
    'ws_44': {
        'name': '44',
        'title': 'Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
        'desc': 'Stories where issues of gender equality/inequality are raised by sex of reporter and by region',
        'reports': ['global', 'region'],
        'historical': '16cF'
    },
    'ws_45': {
        'name': '45',
        'title': 'Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
        'desc': 'Stories where issues of gender equality/inequality are raised by sex of \'people in the news\' and by region',
        'reports': ['global', 'region'],
        'historical': '16dF'
    },
    'ws_46': {
        'name': '46',
        'title': 'Story clearly challenges gender stereotypes by region by major news topic',
        'desc': 'Stories where stereotypes are challenged/ supported by news topic',
        'reports': ['global'],
    },
    'ws_47': {
        'name': '47',
        'title': 'Story clearly challenges gender stereotypes by major topic',
        'desc': 'Stories where stereotypes are challenged/ supported by topic',
        'reports': ['global', 'region', 'country'],
    },
    'ws_48': {
        'name': '48',
        'title': 'Story clearly challenges gender stereotypes by sex of rep',
        'desc': 'Stories where stereotypes are challenged/ supported by gender of rep',
        'reports': ['global', 'region', 'country'],
    },
    'ws_49': {
        'name': '49',
        'title': 'Internet - Main topics by region',
        'desc': 'Internet - Main topics by region',
        'reports': ['global', 'region', 'country'],
    },
    'ws_50': {
        'name': '50',
        'title': 'Internet - Story shared on Twitter',
        'desc': 'Internet - Story shared on Twitter',
        'reports': ['global', 'country'],
    },
    'ws_51': {
        'name': '51',
        'title': 'Internet - Story shared on Facebook',
        'desc': 'Internet - Story shared on Facebook',
        'reports': ['global', 'country'],
    },
    'ws_52': {
        'name': '52',
        'title': 'Internet - Reference to gender equality/HR policies',
        'desc': 'Internet - Reference to gender equality/HR policies',
        'reports': ['global', 'country'],
    },
    'ws_53': {
        'name': '53',
        'title': 'Internet - Female reporters in main stories',
        'desc': 'Internet - Female reporters in main stories',
        'reports': ['global', 'region', 'country']
    },
    'ws_54': {
        'name': '54',
        'title': 'Internet - Overall presence of women',
        'desc': 'Internet - Overall presence of women',
        'reports': ['global', 'region', 'country']
    },
    'ws_55': {
        'name': '55',
        'title': 'Internet - Occupation of Female news subjects',
        'desc': 'Internet - Occupation of Female news subjects',
        'reports': ['global'],
    },
    'ws_56': {
        'name': '56',
        'title': 'Internet - Functions of news subjects',
        'desc': 'Internet - Functions of news subjects',
        'reports': ['global', 'region', 'country'],
    },
    'ws_57': {
        'name': '57',
        'title': 'Internet - News subjects who are identified by family status',
        'desc': 'Internet - News subjects who are identified by family status',
        'reports': ['global', 'country'],
    },
    'ws_58': {
        'name': '58',
        'title': 'Internet - News subjects in multimedia web components',
        'desc': 'Internet - News subjects in multimedia web components',
        'reports': ['global', 'country'],
    },
    'ws_59': {
        'name': '59',
        'title': 'Internet - Selection of News Subjects',
        'desc': 'Internet - Selection of News Subjects by sex of reporter (columns) and sex of subject (rows)',
        'reports': ['global', 'country'],
    },
    'ws_60': {
        'name': '60',
        'title': 'Internet - Age of news subjects',
        'desc': 'Internet - Age of news subjects',
        'reports': ['global', 'country'],
    },
    'ws_61': {
        'name': '61',
        'title': 'Internet - News subjects who are directly quoted',
        'desc': 'Internet - News subjects who are directly quoted',
        'reports': ['global', 'country'],
    },
    'ws_62': {
        'name': '62',
        'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'desc': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'reports': ['global', 'region', 'country'],
    },
    'ws_63': {
        'name': '63',
        'title': 'Internet -Stories where stereotypes are clearly challenged',
        'desc': 'Internet -Stories where stereotypes are clearly challenged',
        'reports': ['global', 'region', 'country'],
    },
    'ws_64': {
        'name': '64',
        'title': 'Internet -Stories with Women as a central Focus',
        'desc': 'Internet -Stories with Women as a central Focus',
        'reports': ['global', 'region', 'country'],
    },
    'ws_65': {
        'name': '65',
        'title': 'Twitter - Original tweet or retweet',
        'desc': 'Twitter - Original tweet or retweet',
        'reports': ['global', 'region', 'country'],
    },
    'ws_66': {
        'name': '66',
        'title': 'Twitter - Overall presence of women',
        'desc': 'Twitter - Overall presence of women',
        'reports': ['global', 'region', 'country'],
    },
    'ws_67': {
        'name': '67',
        'title': 'Twitter - Female reporters & journalists',
        'desc': 'Twitter - Female reporters & journalists',
        'reports': ['global', 'region', 'country'],
    },
    'ws_68': {
        'name': '68',
        'title': 'Twitter - Women\'s centrality',
        'desc': 'Twitter - Women\'s centrality',
        'reports': ['global', 'region', 'country'],
    },
    'ws_68b': {
        'name': '68b',
        'title': 'Twitter - Challenging Stereotypes',
        'desc': 'Twitter - Challenging Stereotypes',
        'reports': ['global', 'region', 'country'],
    },
    'ws_70': {
        'name': '70',
        'title': 'Twitter - Hashtags',
        'desc': 'Twitter - Hashtags',
        'reports': ['global']
    },
    'ws_71': {
        'name': '71',
        'title': 'Key themes, women\'s overall presence',
        'desc': 'Key themes, women\'s overall presence',
        'reports': ['global', 'region', 'country'],
    },
    'ws_72': {
        'name': '72',
        'title': 'Key themes, female reporters',
        'desc': 'Key themes, female reporters',
        'reports': ['global', 'region', 'country'],
    },
    'ws_73': {
        'name': '73',
        'title': 'Key themes, selection of sources by sex of reporter',
        'desc': 'Key themes, selection of sources by sex of reporter',
        'reports': ['global', 'region', 'country'],
    },
    'ws_74': {
        'name': '74',
        'title': 'Key themes, women\'s centrality',
        'desc': 'Stories with Women as a central focus, by women centrality topic',
        'reports': ['global', 'region', 'country'],
    },
    'ws_75': {
        'name': '75',
        'title': 'Key themes, challenging stereotypes',
        'desc': 'Key themes, challenging stereotypes',
        'reports': ['global', 'region', 'country'],
    },
    'ws_76': {
        'name': '76',
        'title': 'Key themes, reference to gender equality/HR policies',
        'desc': 'Key themes, reference to gender equality/HR policies',
        'reports': ['global', 'region', 'country'],
    },
    'ws_77': {
        'name': '77',
        'title': 'Key themes, portrayal as victims',
        'desc': 'Key themes, portrayal as victims',
        'reports': ['global', 'region', 'country'],
    },
    'ws_78': {
        'name': '78',
        'title': 'Key themes, portrayal as survivors',
        'desc': 'Key themes, portrayal as survivors',
        'reports': ['global', 'region', 'country'],
    },
    'ws_79': {
        'name': '79',
        'title': 'Internet - Main topics by region',
        'desc': 'Internet - Main topics by region',
        'reports': ['global'],
    },
    'ws_80': {
        'name': '80',
        'title': 'Internet - Story shared on Twitter',
        'desc': 'Internet - Story shared on Twitter',
        'reports': ['global'],
    },
    'ws_81': {
        'name': '81',
        'title': 'Internet - Story shared on Facebook',
        'desc': 'Internet - Story shared on Facebook',
        'reports': ['global'],
    },
    'ws_82': {
        'name': '82',
        'title': 'Internet - Reference to gender equality/HR policies',
        'desc': 'Internet - Reference to gender equality/HR policies',
        'reports': ['global'],
    },
    'ws_83': {
        'name': '83',
        'title': 'Internet - reporters in main stories',
        'desc': 'Internet - reporters in main stories',
        'reports': ['global'],
    },
    'ws_84': {
        'name': '84',
        'title': 'Internet - Occupation of Female news subjects',
        'desc': 'Internet - Occupation of Female news subjects',
        'reports': ['global'],
    },
    'ws_85': {
        'name': '85',
        'title': 'Internet - Functions of news subjects',
        'desc': 'Internet - Functions of news subjects',
        'reports': ['global'],
    },
    'ws_86': {
        'name': '86',
        'title': 'Internet - News subjects who are identified by family status',
        'desc': 'Internet - News subjects who are identified by family status',
        'reports': ['global'],
    },
    'ws_87': {
        'name': '87',
        'title': 'Internet - News subjects in multimedia web components',
        'desc': 'Internet - News subjects in multimedia web components',
        'reports': ['global'],
    },
    'ws_88': {
        'name': '88',
        'title': 'Internet - Selection of News Subjects',
        'desc': 'Internet - Selection of News Subjects',
        'reports': ['global'],
    },
    'ws_89': {
        'name': '89',
        'title': 'Internet - Age of news subjects',
        'desc': 'Internet - Age of news subjects',
        'reports': ['global'],
    },
    'ws_90': {
        'name': '90',
        'title': 'Internet - News subjects who are directly quoted',
        'desc': 'Internet - News subjects who are directly quoted',
        'reports': ['global'],
    },
    'ws_91': {
        'name': '91',
        'title': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'desc': 'Internet - Stories where issues of gender equality/inequality are raised by topic',
        'reports': ['global'],
    },
    'ws_92': {
        'name': '92',
        'title': 'Internet -Stories where stereotypes are clearly challenged',
        'desc': 'Internet -Stories where stereotypes are clearly challenged',
        'reports': ['global'],
    },
    'ws_93': {
        'name': '93',
        'title': 'Internet -Stories with Women as a central Focus',
        'desc': 'Internet -Stories with Women as a central Focus',
        'reports': ['global'],
    },
    'ws_94': {
        'name': '94',
        'title': 'Twitter - Original tweet or retweet',
        'desc': 'Twitter - Original tweet or retweet',
        'reports': ['global'],
    },
    'ws_95': {
        'name': '95',
        'title': 'Twitter - Female reporters',
        'desc': 'Twitter - Female reporters',
        'reports': ['global'],
    },
    'ws_96': {
        'name': '96',
        'title': 'Twitter - Women\'s centrality',
        'desc': 'Twitter - Women\'s centrality',
        'reports': ['global'],
    },
    'ws_97': {
        'name': '97',
        'title': 'Twitter - Challenging Stereotypes',
        'desc': 'Twitter - Challenging Stereotypes',
        'reports': ['global'],
    },
    'ws_s01': {
        'name': 's01',
        'title': 'Sex of presenters, reporters and news subjects',
        'desc': 'Sex of presenters, reporters and news subjects',
        'reports': ['global'],
    },
    'ws_s02': {
        'name': 's02',
        'title': 'News subjects in television, radio and newspapers',
        'desc': 'News subjects in television, radio and newspapers',
        'reports': ['global'],
    },
    'ws_s03': {
        'name': 's03',
        'title': 'News subjects in major topic areas',
        'desc': 'News subjects in major topic areas',
        'reports': ['global'],
    },
    'ws_s04': {
        'name': 's04',
        'title': 'News subjects in major occupational groups',
        'desc': 'News subjects in major occupational groups',
        'reports': ['global'],
    },
    'ws_s05': {
        'name': 's05',
        'title': 'Function of news subjects',
        'desc': 'Function of news subjects',
        'reports': ['global'],
    },
    'ws_s06': {
        'name': 's06',
        'title': 'News subjects who are victims',
        'desc': 'News subjects who are victims',
        'reports': ['global'],
    },
    'ws_s07': {
        'name': 's07',
        'title': 'News subjects mentioned by family status',
        'desc': 'News subjects mentioned by family status',
        'reports': ['global'],
    },
    'ws_s08': {
        'name': 's08',
        'title': 'News subjects quoted in newspapers',
        'desc': 'News subjects quoted in newspapers',
        'reports': ['global'],
    },
    'ws_s09': {
        'name': 's09',
        'title': 'News subjects appearing in newspaper photographs',
        'desc': 'News subjects appearing in newspaper photographs',
        'reports': ['global'],
    },
    'ws_s10': {
        'name': 's10',
        'title': 'Presenters and reporters in television, radio and newspapers',
        'desc': 'Presenters and reporters in television, radio and newspapers',
        'reports': ['global'],
    },
    'ws_s11': {
        'name': 's11',
        'title': 'Reporters in major topic areas',
        'desc': 'Reporters in major topic areas',
        'reports': ['global'],
    },
    'ws_s12': {
        'name': 's12',
        'title': 'Topics in stories where women are central to the news',
        'desc': 'Topics in stories where women are central to the news',
        'reports': ['global'],
    },
    'ws_s13': {
        'name': 's13',
        'title': 'Sex of reporter in stories with female and male news subjects',
        'desc': 'Sex of reporter in stories with female and male news subjects',
        'reports': ['global'],
    },
    'ws_s14': {
        'name': 's14',
        'title': 'Stories that clearly challenge stereotypes',
        'desc': 'Stories that clearly challenge stereotypes',
        'reports': ['global'],
    },
    'ws_s15': {
        'name': 's15',
        'title': 'Stories that highlight gender equality or inequality',
        'desc': 'Stories that highlight gender equality or inequality',
        'reports': ['global'],
    },
    'ws_s16': {
        'name': 's16',
        'title': 'Stories that mention human rights or equality legislation and policies',
        'desc': 'Stories that mention human rights or equality legislation and policies',
        'reports': ['global'],
    },
    'ws_s17': {
        'name': 's17',
        'title': 'Internet, Twitter - Sex of reporters and news subjects',
        'desc': 'Internet, Twitter - Sex of reporters and news subjects',
        'reports': ['global'],
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
    ('5', [42, 43, 44, 45, 46, 47, 48]),
    ('6', [49, 50, 51, 52, 53, 54]),
    ('7', [55])
])

TOPIC_GROUPS = {
    1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1,
    8: 2, 9: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 16: 2, 17: 2, 18: 2,
    19: 3, 20: 3, 21: 3, 22: 3, 23: 3, 24: 3, 25: 3, 26: 3, 27: 3,
    28: 4, 29: 4, 30: 4, 31: 4, 32: 4, 33: 4, 34: 4, 35: 4, 36: 4, 37: 4, 38: 4, 39: 4, 40: 4, 41: 4,
    42: 5, 43: 5, 44: 5, 45: 5, 46: 5, 47: 5, 48: 5,
    49: 6, 50: 6, 51: 6, 52: 6, 53: 6, 54: 6,
    55: 7
}

MAJOR_TOPICS = (
    (1, 'Politics and Government'),
    (2, 'Economy'),
    (3, 'Science and Health'),
    (4, 'Social and Legal'),
    (5, 'Crime and Violence'),
    (6, 'Celebrity, Arts and Media, Sports'),
    (7, 'Other')
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

FOCUS_TOPIC_ID_MAP = {x: ft for ft, topics in FOCUS_TOPIC_IDS.iteritems() for x in topics}

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
