import re
from django_countries.fields import countries

from sheets.serializers import (
    NewspaperSheet,
    NewspaperPerson,
    NewspaperJournalist,
    InternetNewsSheetSerializer,
    InternetNewsPersonSerializer,
    InternetNewsJournalistSerializer,
    NewspaperSheetSerializer,
    NewspaperPersonSerializer,
    NewspaperJournalistSerializer,
    TwitterSheetSerializer,
    TwitterPersonSerializer,
    TwitterJournalistSerializer,
    RadioSheetSerializer,
    RadioPersonSerializer,
    RadioJournalistSerializer,
    TelevisionSheetSerializer,
    TelevisionPersonSerializer,
    TelevisionJournalistSerializer,
)

def get_all_coding_data(coding_data, row):
    country = countries.alpha2(coding_data.get('countries').get(row)) if coding_data.get('countries') else None
    monitor_code = coding_data.get('monitors').get(row) if coding_data.get('monitors') else None
    newspaper_name = coding_data.get('newspaper_name').get(row) if coding_data.get('newspaper_name') else None
    covid19 = coding_data.get('covid19').get(row) if coding_data.get('covid19') else None
    topic = coding_data.get('topic').get(row) if coding_data.get('topic') else None
    scope = coding_data.get('scope').get(row) if coding_data.get('scope') else None
    space = coding_data.get('space').get(row) if coding_data.get('space') else {}
    equality_rights = coding_data.get('equality_rights').get(row) if coding_data.get('equality_rights') else None
    about_women = coding_data.get('about_women').get(row) if coding_data.get('about_women') else None
    inequality_women = coding_data.get('inequality_women').get(row) if coding_data.get('inequality_women') else None
    stereotypes = coding_data.get('stereotypes').get(row) if coding_data.get('stereotypes') else None
    date = format_date(coding_data.get('time_accessed').get(row).split(' ')[0]) if coding_data.get('time_accessed') else None
    time = format_time(coding_data.get('time_accessed').get(row).split(' ')[1]) if coding_data.get('time_accessed') else None
    website_name = coding_data.get('website_name').get(row) if coding_data.get('website_name') else None
    website_url = coding_data.get('website_url').get(row) if coding_data.get('website_url') else None
    offline_presence = re.findall(r'\d+', coding_data.get('offline_presence').get(row)) if coding_data.get('offline_presence') else ['0']
    webpage_layer_no = coding_data.get('webpage_layer_no').get(row) if coding_data.get('webpage_layer_no') else None
    shared_via_twitter = coding_data.get('shared_via_twitter').get(row) if coding_data.get('shared_via_twitter') else None
    shared_on_facebook = coding_data.get('shared_on_facebook').get(row) if coding_data.get('shared_on_facebook') else None
    equality_rights = coding_data.get('equality_rights').get(row) if coding_data.get('equality_rights') else None
    comments = coding_data.get('comments').get(row) if coding_data.get('comments') else None
    sex = coding_data.get("sex").get(row) if coding_data.get('sex') else None
    age = coding_data.get("age").get(row) if coding_data.get('age') else None
    occupation = coding_data.get("occupation").get(row) if coding_data.get('occupation') else None
    function = coding_data.get("function").get(row) if coding_data.get('function') else None
    family_role = coding_data.get("family_role").get(row) if coding_data.get('family_role') else None
    victim_or_survivor = coding_data.get("victim_or_survivor").get(row) if coding_data.get('victim_or_survivor') else None
    victim_of = coding_data.get("victim_of").get(row) if coding_data.get('victim_of') else None
    survivor_of = coding_data.get("survivor_of").get(row) if coding_data.get('survivor_of') else None
    is_quoted = coding_data.get("is_quoted").get(row) if coding_data.get('is_quoted') else None
    is_photograph = coding_data.get("is_photograph").get(row) if coding_data.get('is_photograph') else None
    special_qn_1 = coding_data.get("special_qn_1").get(row) if coding_data.get('special_qn_1') else None
    special_qn_2 = coding_data.get("special_qn_2").get(row) if coding_data.get('special_qn_2') else None
    special_qn_3 = coding_data.get("special_qn_3").get(row) if coding_data.get('special_qn_3') else None

    return {
        "monitor_mode": 1,
        "country": country,
        "monitor_code": monitor_code,
        "newspaper_name": newspaper_name,
        "website_name": website_name,
        "webpage_layer_no": int(webpage_layer_no) if webpage_layer_no else '',
        "shared_via_twitter": 'Y' if shared_via_twitter == '1' else 'N',
        "shared_on_facebook": 'Y' if shared_on_facebook == '1' else 'N',
        "equality_rights": 'Y' if equality_rights == '1' else 'N',
        "offline_presence": 'Y' if offline_presence[0] == '1' else 'N',
        "time_accessed": f"{date} {time}",
        "website_url": website_url,
        "covid19": int(covid19) if covid19 else '',
        "topic": int(topic) if topic else '',
        "scope": int(scope) if scope else '',
        "space": space,
        "equality_rights": 'Y' if equality_rights == 'Y' else 'N',
        "about_women": 'Y' if about_women == 'Y' else 'N',
        "inequality_women": int(inequality_women) if inequality_women else "",
        "stereotypes": int(stereotypes) if stereotypes else '',
        "url_and_multimedia": comments,
        "sex": int(sex) if sex else None,
        "age": int(age) if age else None,
        "occupation": int(occupation) if occupation else None,
        "function": int(function) if function else None,
        "family_role": 'Y' if family_role == '1' else 'N',
        "victim_or_survivor": 'Y' if victim_or_survivor == '1' else 'N',
        "victim_of": int(victim_of) if victim_of else None,
        "survivor_of": int(survivor_of) if survivor_of else None,
        "is_quoted": 'Y' if is_quoted == '1' else 'N',
        "is_photograph": int(is_photograph) if is_photograph else None,
        "special_qn_1": 'Y' if special_qn_1 == '1' else 'N',
        "special_qn_2": 'Y' if special_qn_2 == '1' else 'N',
        "special_qn_3": 'Y' if special_qn_3 == '1' else 'N',
        "further_analysis": 'N'
    }

def get_people_data(coding_data, row):
    common_data = get_all_coding_data(coding_data, row)

    return {
        "sex": common_data.get("sex"),
        "age": common_data.get("age"),
        "occupation": common_data.get("occupation"),
        "function": common_data.get("function"),
        "family_role": common_data.get("family_role"),
        "victim_or_survivor": common_data.get("victim_or_survivor"),
        "victim_of": common_data.get("victim_of"),
        "survivor_of": common_data.get("survivor_of"),
        "is_quoted": common_data.get("is_quoted"),
        "is_photograph": common_data.get("is_photograph"),
        "special_qn_1": common_data.get("special_qn_1"),
        "special_qn_2": common_data.get("special_qn_2"),
        "special_qn_3": common_data.get("special_qn_3"),
    }

def get_internent_coding_data(internet_coding_data, row):
    common_data = get_all_coding_data(internet_coding_data, row)

    return {
        "monitor_mode": common_data.get('monitor_mode'),
        "country": common_data.get('country'),
        "monitor_code": common_data.get('monitor_code'),
        "website_name": common_data.get('website_name'),
        "website_url": common_data.get('website_url'),
        "time_accessed": common_data.get('time_accessed'),
        "offline_presence": common_data.get('offline_presence'),
        "webpage_layer_no": common_data.get('webpage_layer_no'),
        "covid19": common_data.get('covid19'),
        "topic": common_data.get('topic'),
        "scope": common_data.get('scope'),
        "shared_via_twitter": common_data.get('shared_via_twitter'),
        "shared_on_facebook": common_data.get('shared_on_facebook'),
        "equality_rights": common_data.get('equality_rights'),
        "about_women": common_data.get('about_women'),
        "inequality_women": common_data.get('inequality_women'),
        "stereotypes": common_data.get('stereotypes'),
        "url_and_multimedia": common_data.get('url_and_multimedia'),
        "further_analysis": common_data.get('further_analysis'),
    }

def save_internent_news_data(internet_coding_data, journalist_internet_coding_data):
    if internet_coding_data:
        for row in internet_coding_data.get('countries', []):
            sheet_data = get_internent_coding_data(internet_coding_data, row)

            internet_news_sheet_serializer = InternetNewsSheetSerializer(data=sheet_data)

            if internet_news_sheet_serializer.is_valid():
                internet_news_sheet = internet_news_sheet_serializer.save()
                person_data = {}
                person_data['internetnews_sheet'] = internet_news_sheet.id
                # If next row is current row+1 then that row belongs to this sheet
                # e.g if current row is 2 and next row is 3 then that row holds the second Journalist or the second person in the news.
                while internet_coding_data.get("sex").get(row):
                    people_data = get_people_data(internet_coding_data, row)
                    person_data.update(people_data)

                    internet_news_person_serializer = InternetNewsPersonSerializer(data=person_data)
                    if internet_news_person_serializer.is_valid():
                        internet_news_person_serializer.save()
                    else:
                        self.stdout.write("Error occurred ", internet_news_person_serializer.errors)

                    sex = journalist_internet_coding_data.get("sex").get(row)
                    # age = journalist_internet_coding_data.get("age").get(row)

                    journalist_data = {
                        "sex": int(sex) if sex else None,
                        "age": None,
                        "internetnews_sheet": internet_news_sheet.id
                    }
                    internet_news_journalist_serializer = InternetNewsJournalistSerializer(data=journalist_data)
                    if internet_news_journalist_serializer.is_valid():
                        internet_news_journalist_serializer.save()
                    else:
                        print("Error occurred: Journalist Sex can't be null")
                    row = str(int(row) + 1)

def save_newspaper_news_data(newspaper_coding_data, journalist_newspaper_coding_data):
    if newspaper_coding_data:
        for row in newspaper_coding_data.get('countries', []):
            inequality_women = newspaper_coding_data.get('inequality_women').get(row)
            stereotypes = newspaper_coding_data.get('stereotypes').get(row)

            sheet_data = {
                "monitor_mode": 1,
                "country": countries.alpha2(newspaper_coding_data.get('countries').get(row)),
                "monitor_code": newspaper_coding_data.get('monitors').get(row),
                "newspaper_name": newspaper_coding_data.get('newspaper_name').get(row),
                "page_number": newspaper_coding_data.get('page_number').get(row),
                "covid19": newspaper_coding_data.get('covid19').get(row),
                "topic": newspaper_coding_data.get('topic').get(row),
                "scope": newspaper_coding_data.get('scope').get(row),
                "space": newspaper_coding_data.get('space').get(row),
                "equality_rights": 'Y' if newspaper_coding_data.get('equality_rights').get(row) == '1' else 'N',
                "about_women": 'Y' if newspaper_coding_data.get('about_women').get(row) == '1' else 'N',
                "inequality_women": int(inequality_women) if inequality_women else '',
                "stereotypes": int(stereotypes) if stereotypes else '',
                "further_analysis": 'N',
                "comments": newspaper_coding_data.get('comments').get(row)
            }
            newspaper_news_serializer = NewspaperSheetSerializer(data=sheet_data)
            if newspaper_news_serializer.is_valid():
                newspaper_news = newspaper_news_serializer.save()
                person_data = dict(newspaper_sheet=newspaper_news.id)
                while newspaper_coding_data.get("sex").get(row):
                    person_data.update(get_people_data(newspaper_coding_data, row))
                    newspaper_person_serialiser = NewspaperPersonSerializer(data=person_data)
                    if newspaper_person_serialiser.is_valid():
                        newspaper_person_serialiser.save()
                    else:
                        print("Error occurred ", newspaper_person_serialiser.errors, flush=True)

                    sex = journalist_newspaper_coding_data.get("sex").get(row)
                    journalist_data = {
                        "sex": int(sex) if sex else None,
                        "age": None,
                        "newspaper_sheet": newspaper_news.id,
                    }
                    newspaper_journalist_serializer = NewspaperJournalistSerializer(data=journalist_data)
                    if newspaper_journalist_serializer.is_valid():
                        newspaper_journalist_serializer.save()
                    else:
                        print("Error occurred: Journalist sex can't be null", flush=True)
                    row = str(int(row) + 1)
    else:
        return {}

def save_radio_news_data(radio_coding_data, journalist_radio_coding_data):
    if radio_coding_data:
        for row in radio_coding_data.get('countries', []):
            inequality_women = radio_coding_data.get('inequality_women').get(row)
            stereotypes = radio_coding_data.get('stereotypes').get(row)

            sheet_data = {
                "monitor_mode": 1,
                "country": countries.alpha2(radio_coding_data.get('countries').get(row)),
                "monitor_code": radio_coding_data.get('monitors').get(row),
                "channel": radio_coding_data.get('channel').get(row),
                "start_time": radio_coding_data.get('start_time').get(row),
                "num_female_anchors": radio_coding_data.get('num_female_anchors').get(row),
                "num_male_anchors": radio_coding_data.get('num_male_anchors').get(row),
                "item_number": radio_coding_data.get('item_number').get(row),
                "covid19": radio_coding_data.get('covid19').get(row),
                "topic": 'Y' if radio_coding_data.get('topic').get(row) == '1' else 'N',
                "scope": 'Y' if radio_coding_data.get('scope').get(row) == '1' else 'N',
                "equality_rights": 'Y' if radio_coding_data.get('equality_rights').get(row) == '1' else 'N',
                "about_women": 'Y' if radio_coding_data.get('about_women').get(row) == '1' else 'N',
                "inequality_women": int(inequality_women) if inequality_women else '',
                "stereotypes": int(stereotypes) if stereotypes else '',
                "further_analysis": 'N',
                "comments": radio_coding_data.get('comments').get(row),
            }
            radio_news_serializer = RadioSheetSerializer(data=sheet_data)
            if radio_news_serializer.is_valid():
                radio_news = radio_news_serializer.save()
                person_data = dict(radio_sheet=radio_news.id)
                while radio_coding_data.get("sex").get(row):
                    person_data.update(get_people_data(radio_coding_data, row))
                    radio_person_serialiser = RadioPersonSerializer(data=person_data)
                    if radio_person_serialiser.is_valid():
                        radio_person_serialiser.save()
                    else:
                        print("Error occurred ", radio_person_serialiser.errors, flush=True)

                    sex = journalist_radio_coding_data.get("sex").get(row)
                    journalist_data = {
                        "sex": int(sex) if sex else None,
                        "role": None,
                        "radio_sheet": radio_news.id,
                    }
                    radio_journalist_serializer = RadioJournalistSerializer(data=journalist_data)
                    if radio_journalist_serializer.is_valid():
                        radio_journalist_serializer.save()
                    else:
                        print("Error occurred: Journalist sex can't be null", flush=True)
                    row = str(int(row) + 1)


def save_tv_news_data(tv_coding_data, journalist_tv_coding_data):
    if tv_coding_data:
        for row in tv_coding_data.get('countries', []):
            inequality_women = tv_coding_data.get('inequality_women').get(row)
            stereotypes = tv_coding_data.get('stereotypes').get(row)

            sheet_data = {
                "monitor_mode": 1,
                "country": countries.alpha2(tv_coding_data.get('countries').get(row)),
                "monitor_code": tv_coding_data.get('monitors').get(row),
                "channel": tv_coding_data.get('channel').get(row),
                "start_time": tv_coding_data.get('start_time').get(row),
                "num_female_anchors": tv_coding_data.get('num_female_anchors').get(row),
                "num_male_anchors": tv_coding_data.get('num_male_anchors').get(row),
                "item_number": tv_coding_data.get('item_number').get(row),
                "covid19": tv_coding_data.get('covid19').get(row),
                "topic": 'Y' if tv_coding_data.get('topic').get(row) == '1' else 'N',
                "scope": 'Y' if tv_coding_data.get('scope').get(row) == '1' else 'N',
                "equality_rights": 'Y' if tv_coding_data.get('equality_rights').get(row) == '1' else 'N',
                "about_women": 'Y' if tv_coding_data.get('about_women').get(row) == '1' else 'N',
                "inequality_women": int(inequality_women) if inequality_women else '',
                "stereotypes": int(stereotypes) if stereotypes else '',
                "further_analysis": 'N',
                "comments": tv_coding_data.get('comments').get(row),
            }
            tv_news_serializer = TelevisionSheetSerializer(data=sheet_data)
            if tv_news_serializer.is_valid():
                tv_news = tv_news_serializer.save()
                person_data = dict(television_sheet=tv_news.id)
                while tv_coding_data.get("sex").get(row):
                    person_data.update(get_people_data(tv_coding_data, row))
                    tv_person_serialiser = TelevisionPersonSerializer(data=person_data)
                    if tv_person_serialiser.is_valid():
                        tv_person_serialiser.save()
                    else:
                        print("Error occurred ", tv_person_serialiser.errors, flush=True)

                    sex = journalist_tv_coding_data.get("sex").get(row)
                    journalist_data = {
                        "sex": int(sex) if sex else None,
                        "age": None,
                        "role": None,
                        "television_sheet": tv_news.id,
                    }
                    tv_journalist_serializer = TelevisionJournalistSerializer(data=journalist_data)
                    if tv_journalist_serializer.is_valid():
                        tv_journalist_serializer.save()
                    else:
                        print("Error occurred: Journalist sex can't be null", flush=True)
                    row = str(int(row) + 1)

def save_twitter_news_data(twitter_coding_data, journalist_twitter_coding_data):
    if twitter_coding_data:
        for row in twitter_coding_data.get('countries', []):
            inequality_women = twitter_coding_data.get('inequality_women').get(row)
            stereotypes = twitter_coding_data.get('stereotypes').get(row)

            about_women_data = twitter_coding_data.get('about_women')
            if about_women_data:
                about_women = 'Y' if about_women_data.get(row) == '1' else 'N'
            else:
                about_women = 'N'

            sheet_data = {
                "monitor_mode": 1,
                "country": countries.alpha2(twitter_coding_data.get('countries').get(row)),
                "monitor_code": twitter_coding_data.get('monitors').get(row),
                "media_name": twitter_coding_data.get('media_name').get(row),
                "twitter_handle": twitter_coding_data.get('twitter_handle').get(row),
                "retweet": twitter_coding_data.get('retweet').get(row),
                "covid19": twitter_coding_data.get('covid19').get(row),
                "topic": 'Y' if twitter_coding_data.get('topic').get(row) == '1' else 'N',
                "equality_rights": 'Y' if twitter_coding_data.get('equality_rights').get(row) == '1' else 'N',
                "about_women": about_women,
                "inequality_women": int(inequality_women) if inequality_women else '',
                "stereotypes": int(stereotypes) if stereotypes else '',
                "further_analysis": 'N',
                "url_and_multimedia": twitter_coding_data.get('comments').get(row),
            }
            twitter_news_serializer = TwitterSheetSerializer(data=sheet_data)
            if twitter_news_serializer.is_valid():
                twitter_news = twitter_news_serializer.save()
                person_data = dict(twitter_sheet=twitter_news.id)
                while twitter_coding_data.get("sex").get(row):
                    person_data.update(get_people_data(twitter_coding_data, row))
                    twitter_person_serialiser = TwitterPersonSerializer(data=person_data)
                    if twitter_person_serialiser.is_valid():
                        twitter_person_serialiser.save()
                    else:
                        print("Error occurred ", twitter_person_serialiser.errors, flush=True)

                    sex = journalist_twitter_coding_data.get("sex").get(row)
                    journalist_data = {
                        "sex": int(sex) if sex else None,
                        "age": None,
                        "twitter_sheet": twitter_news.id,
                    }
                    twitter_journalist_serializer = TwitterJournalistSerializer(data=journalist_data)
                    if twitter_journalist_serializer.is_valid():
                        twitter_journalist_serializer.save()
                    else:
                        print("Error occurred: Journalist sex can't be null", flush=True)
                    row = str(int(row) + 1)


def merge_data(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_data(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def get_common_coding_data(data):
    # This gives you data for the whole sheet. e.g {"countries": {row1, row2, row3, ..., rowN}}
    # You will thus be required to further extract data for individual rows while saving the data into the database
    # e.g .get('countries').get(row)
    rows = [x for x in data['country_code']]
    if not rows:
        return None
    return {
        "countries": data.get('country_code'),
        "monitors": data.get('monitor_code'),
        "covid19": data.get('covid19'),
        "scope": data.get('scope'),
        "topic": data.get('topic'),
        "equality_rights": data.get('equality_rights'),
        "about_women": data.get('about_women'),
        "inequality_women": data.get('inequality_women'),
        "stereotypes": data.get('stereotypes'),
        "comments": data.get('comments'),
        "story_label": data.get('story_label'),
        "sex": data.get('sex'),
        "age": data.get('age'),
        "occupation": data.get('occupation'),
        "function": data.get('function'),
        "family_role": data.get('family_role'),
        "victim_or_survivor": data.get('victim_or_survivor'),
        "victim_of": data.get('victim_of'),
        "survivor_of": data.get('survivor_of'),
        "is_quoted": data.get('is_quoted'),
        "is_photograph": data.get('is_photograph'),
        "special_qn_1": data.get('special_qn_1'),
        "special_qn_2": data.get('special_qn_2'),
        "special_qn_3": data.get('special_qn_3'),
    }

def get_newspaper_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []
    common_coding_data['newspaper_name'] = data.get('newspaper_name')
    common_coding_data['page_number'] = data.get('page_number')
    common_coding_data['space'] = data.get('space')

    return common_coding_data

def get_radio_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []
    common_coding_data['channel'] = data.get('channel')
    common_coding_data['start_time'] = data.get('start_time')
    common_coding_data['num_female_anchors'] = data.get('num_female_anchors')
    common_coding_data['num_male_anchors'] = data.get('num_male_anchors')
    common_coding_data['item_number'] = data.get('item_number')

    return common_coding_data

def get_tv_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []

    common_coding_data['channel'] = data.get('channel')
    common_coding_data['start_time'] = data.get('start_time')
    common_coding_data['num_female_anchors'] = data.get('num_female_anchors')
    common_coding_data['num_male_anchors'] = data.get('num_male_anchors')
    common_coding_data['item_number'] = data.get('item_number')

    return common_coding_data

def get_internet_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []

    common_coding_data['website_name'] = data.get('website_name')
    common_coding_data['website_url'] = data.get('website_url')
    common_coding_data['time_accessed'] = data.get('time_accessed')
    common_coding_data['offline_presence'] = data.get('offline_presence')
    common_coding_data['webpage_layer_no'] = data.get('webpage_layer_no')
    common_coding_data['shared_via_twitter'] = data.get('shared_via_twitter')
    common_coding_data['shared_on_facebook'] = data.get('shared_via_facebook')

    return common_coding_data

def get_twitter_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []
    common_coding_data['twitter_handle'] = data.get('twitter_handle')
    common_coding_data['retweet'] = data.get('retweet')
    common_coding_data['media_name'] = data.get('media_name')

    return common_coding_data

def format_date(date):
    date = date.split(".")
    date.reverse()
    date = '-'.join(date)
    return date.strip()

def format_time(time):
    time = time.replace(".", ":")
    return time.strip()
