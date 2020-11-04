import re
from django_countries.fields import countries

from sheets.serializers import InternetNewsSheetSerializer, InternetNewsPersonSerializer, InternetNewsJournalistSerializer

def save_internent_news_data(internet_coding_data, journalist_internet_coding_data):
    for row in internet_coding_data.get('countries', []):
        date = format_date(internet_coding_data.get('time_accessed').get(row).split('  ')[0])
        time = format_time(internet_coding_data.get('time_accessed').get(row).split('  ')[1])

        webpage_layer_no = internet_coding_data.get('webpage_layer_no').get(row)
        covid19 = internet_coding_data.get('covid19').get(row)
        topic = internet_coding_data.get('topic').get(row)
        scope = internet_coding_data.get('scope').get(row)
        inequality_women = internet_coding_data.get('inequality_women').get(row)
        stereotypes = internet_coding_data.get('stereotypes').get(row)
        url_and_multimedia = internet_coding_data.get('comments').get(row)

        sheet_data = {
            "monitor_mode": 1,
            "country": countries.alpha2(internet_coding_data.get('countries').get(row)),
            "monitor_code": internet_coding_data.get('monitors').get(row),
            "website_name": internet_coding_data.get('website_name').get(row),
            "website_url": internet_coding_data.get('website_url').get(row),
            "time_accessed": f"{date} {time}",
            "offline_presence": 'Y' if re.findall(r'\d+', internet_coding_data.get('offline_presence').get(row))[0] == '1' else 'N',
            "webpage_layer_no": int(webpage_layer_no) if webpage_layer_no else '',
            "covid19": int(covid19) if covid19 else '',
            "topic": int(topic) if topic else '',
            "scope": int(scope) if scope else '',
            "shared_via_twitter": 'Y' if internet_coding_data.get('shared_via_twitter').get(row) == '1' else 'N',
            "shared_on_facebook": 'Y' if internet_coding_data.get('shared_on_facebook').get(row) == '1' else 'N',
            "equality_rights": 'Y' if internet_coding_data.get('equality_rights').get(row) == '1' else 'N',
            "about_women": 'Y' if internet_coding_data.get('about_women').get(row) == '1' else 'N',
            "inequality_women": int(inequality_women) if inequality_women else '',
            "stereotypes": int(stereotypes) if stereotypes else '',
            "url_and_multimedia": url_and_multimedia,
            "further_analysis": 'N'
        }
        
        internet_news_sheet_serializer = InternetNewsSheetSerializer(data=sheet_data)

        if internet_news_sheet_serializer.is_valid():
            internet_news_sheet = internet_news_sheet_serializer.save()
            person_data = {}
            person_data['internetnews_sheet'] = internet_news_sheet.id
            # If next row is current row+1 then that row belongs to this sheet
            # e.g if current row is 2 and next row is 3 then that row holds the second Journalist or the second person in the news.
            while internet_coding_data.get("sex").get(row):
                sex = internet_coding_data.get("sex").get(row)
                age = internet_coding_data.get("age").get(row)
                occupation = internet_coding_data.get("occupation").get(row)
                function = internet_coding_data.get("function").get(row)
                family_role = internet_coding_data.get("family_role").get(row)
                victim_or_survivor = internet_coding_data.get("victim_or_survivor").get(row)
                victim_of = internet_coding_data.get("victim_of").get(row)
                survivor_of = internet_coding_data.get("survivor_of").get(row)
                is_quoted = internet_coding_data.get("is_quoted").get(row)
                is_photograph = internet_coding_data.get("is_photograph").get(row)
                special_qn_1 = internet_coding_data.get("special_qn_1").get(row)
                special_qn_2 = internet_coding_data.get("special_qn_2").get(row)
                special_qn_3 = internet_coding_data.get("special_qn_3").get(row)

                person_data.update({
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
                    "special_qn_3": 'Y' if special_qn_3 == '1' else 'N'
                })
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

def save_newspaper_news_data():
    pass

def save_radio_news_data():
    pass

def save_tv_news_data():
    pass

def save_twitter_news_data():
    pass


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
    common_coding_data['num_female_anchors'] = data.get('num_female_anchors')
    common_coding_data['num_male_anchors'] = data.get('num_male_anchors')
    common_coding_data['item_number'] = data.get('item_number')

    return common_coding_data

def format_date(date):
    date = date.split(".")
    date.reverse()
    date = '-'.join(date)
    return date

def format_time(time):
    time = time.replace(".", ":")
    return time
