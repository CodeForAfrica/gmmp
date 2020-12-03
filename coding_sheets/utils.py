import re
from datetime import datetime
from django_countries.fields import countries

from coding_sheets.models import (
    ProcessedSheet,
    UnProccessedRow,
)
from coding_sheets.serializers import (
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
    country = (
        countries.alpha2(coding_data.get("countries").get(row))
        if coding_data.get("countries")
        else None
    )
    monitor_code = (
        coding_data.get("monitors").get(row) if coding_data.get("monitors") else None
    )
    monitor_mode = (
        coding_data.get("monitor_mode").get(row)
        if coding_data.get("monitor_mode")
        else "long monitoring"
    )

    if monitor_mode.lower() == "short monitoring":
        monitor_mode = 2
    else:
        monitor_mode = 1

    newspaper_name = (
        coding_data.get("newspaper_name").get(row)
        if coding_data.get("newspaper_name")
        else None
    )
    covid19 = (
        coding_data.get("covid19").get(row) if coding_data.get("covid19") else None
    )
    topic = coding_data.get("topic").get(row) if coding_data.get("topic") else None
    scope = coding_data.get("scope").get(row) if coding_data.get("scope") else None
    space = coding_data.get("space").get(row) if coding_data.get("space") else None
    channel = coding_data.get("channel").get(row) if coding_data.get("channel") else ""
    item_number = (
        coding_data.get("item_number").get(row)
        if coding_data.get("item_number")
        else None
    )
    media_name = (
        coding_data.get("media_name").get(row) if coding_data.get("media_name") else ""
    )
    twitter_handle = (
        coding_data.get("twitter_handle").get(row)
        if coding_data.get("twitter_handle")
        else ""
    )
    retweet = (
        coding_data.get("retweet").get(row) if coding_data.get("retweet") else None
    )
    page_number = (
        coding_data.get("page_number").get(row)
        if coding_data.get("page_number")
        else None
    )
    about_women = (
        coding_data.get("about_women").get(row)
        if coding_data.get("about_women")
        else None
    )
    inequality_women = (
        coding_data.get("inequality_women").get(row)
        if coding_data.get("inequality_women")
        else None
    )
    stereotypes = (
        coding_data.get("stereotypes").get(row)
        if coding_data.get("stereotypes")
        else None
    )
    website_name = (
        coding_data.get("website_name").get(row)
        if coding_data.get("website_name")
        else None
    )
    website_url = (
        coding_data.get("website_url").get(row)
        if coding_data.get("website_url")
        else None
    )
    offline_presence = (
        coding_data.get("offline_presence").get(row)
        if coding_data.get("offline_presence")
        else None
    )
    webpage_layer_no = (
        coding_data.get("webpage_layer_no").get(row)
        if coding_data.get("webpage_layer_no")
        else None
    )
    shared_via_twitter = (
        coding_data.get("shared_via_twitter").get(row)
        if coding_data.get("shared_via_twitter")
        else None
    )
    shared_on_facebook = (
        coding_data.get("shared_on_facebook").get(row)
        if coding_data.get("shared_on_facebook")
        else None
    )
    equality_rights = (
        coding_data.get("equality_rights").get(row)
        if coding_data.get("equality_rights")
        else None
    )
    sex = coding_data.get("sex").get(row) if coding_data.get("sex") else None
    age = coding_data.get("age").get(row) if coding_data.get("age") else None
    num_female_anchors = (
        coding_data.get("num_female_anchors").get(row)
        if coding_data.get("num_female_anchors")
        else None
    )
    num_male_anchors = (
        coding_data.get("num_male_anchors").get(row)
        if coding_data.get("num_male_anchors")
        else None
    )
    occupation = (
        coding_data.get("occupation").get(row)
        if coding_data.get("occupation")
        else None
    )
    function = (
        coding_data.get("function").get(row) if coding_data.get("function") else None
    )
    family_role = (
        coding_data.get("family_role").get(row)
        if coding_data.get("family_role")
        else None
    )
    victim_or_survivor = (
        coding_data.get("victim_or_survivor").get(row)
        if coding_data.get("victim_or_survivor")
        else None
    )
    victim_of = (
        coding_data.get("victim_of").get(row) if coding_data.get("victim_of") else None
    )
    survivor_of = (
        coding_data.get("survivor_of").get(row)
        if coding_data.get("survivor_of")
        else None
    )
    is_quoted = (
        coding_data.get("is_quoted").get(row) if coding_data.get("is_quoted") else None
    )
    is_photograph = (
        coding_data.get("is_photograph").get(row)
        if coding_data.get("is_photograph")
        else None
    )
    special_qn_1 = yes_no(
        coding_data.get("special_qn_1").get(row)
        if coding_data.get("special_qn_1")
        else None
    )
    special_qn_2 = yes_no(
        coding_data.get("special_qn_2").get(row)
        if coding_data.get("special_qn_2")
        else None
    )
    special_qn_3 = yes_no(
        coding_data.get("special_qn_3").get(row)
        if coding_data.get("special_qn_3")
        else None
    )
    further_analysis = (
        coding_data.get("further_analysis").get(row)
        if coding_data.get("further_analysis")
        else None
    )
    time_accessed = None
    if coding_data.get("time_accessed"):
        date_time_accessed = coding_data.get("time_accessed").get(row)
        if date_time_accessed:
            date_time_accessed = datetime.fromtimestamp(
                int(str(date_time_accessed)[:10])
            )
            time_accessed = format_date_time(date_time_accessed)
    start_time = (
        coding_data.get("start_time").get(row)
        if coding_data.get("start_time")
        else None
    )
    if start_time:
        start_time = datetime.fromtimestamp(int(str(start_time)[:10]))
        start_time = f"{start_time.hour}:{start_time.minute}"

    # Start Comment Merge Block
    # merge all comment strings across multiple cells belonging to the same story
    # into one long string
    key = int(row)
    comments = coding_data.get("comments") if coding_data.get("comments") else {}
    merged_comment = comments.get(row) if comments.get(row) else ""
    for comment in comments:
        comment_id = int(comment)
        if comment_id <= key:
            continue
        if comment_id > key and comment_id - key == 1:
            merged_comment += (
                f" {comments.get(str(key + 1))}"
                if comments.get(str(key + 1)) != None
                else ""
            )
            key += 1
    # End Comment Merge Block

    return {
        "monitor_mode": monitor_mode,
        "country": country,
        "monitor_code": monitor_code,
        "newspaper_name": newspaper_name,
        "website_name": website_name,
        "webpage_layer_no": int(webpage_layer_no) if webpage_layer_no else None,
        "shared_via_twitter": "Y" if shared_via_twitter == "1" else "N",
        "shared_on_facebook": "Y" if shared_on_facebook == "1" else "N",
        "equality_rights": "Y" if equality_rights == "1" else "N",
        "offline_presence": "Y" if offline_presence == "1" else "N",
        "time_accessed": time_accessed,
        "website_url": website_url,
        "covid19": int(covid19) if covid19 else "",
        "topic": int(topic) if topic else "",
        "scope": int(scope) if scope else "",
        "item_number": int(item_number) if item_number else None,
        "num_female_anchors": int(num_female_anchors) if num_female_anchors else 0,
        "num_male_anchors": int(num_male_anchors) if num_male_anchors else 0,
        "space": space,
        "page_number": page_number,
        "channel": channel,
        "start_time": start_time,
        "media_name": media_name,
        "twitter_handle": twitter_handle,
        "retweet": retweet,
        "about_women": "Y" if about_women == "Y" else "N",
        "inequality_women": int(inequality_women) if inequality_women else "",
        "stereotypes": int(stereotypes) if stereotypes else "",
        "url_and_multimedia": merged_comment or "N/A",
        "comments": merged_comment or "N/A",
        "sex": int(sex) if sex else None,
        "age": int(age) if age else None,
        "occupation": int(occupation) if occupation else None,
        "function": int(function) if function else None,
        "family_role": "Y" if family_role == "1" else "N",
        "victim_or_survivor": "Y" if victim_or_survivor == "1" else "N",
        "victim_of": int(victim_of) if victim_of else None,
        "survivor_of": int(survivor_of) if survivor_of else None,
        "is_quoted": "Y" if is_quoted == "1" else "N",
        "is_photograph": int(is_photograph) if is_photograph else None,
        "special_qn_1": special_qn_1,
        "special_qn_2": special_qn_2,
        "special_qn_3": special_qn_3,
        "further_analysis": "Y" if further_analysis == "1" else "N",
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


def get_data_for_newspaper_coding(newspaper_coding_data, row):
    common_data = get_all_coding_data(newspaper_coding_data, row)

    return {
        "monitor_mode": common_data.get("monitor_mode"),
        "country": common_data.get("country"),
        "monitor_code": common_data.get("monitor_code"),
        "newspaper_name": common_data.get("newspaper_name"),
        "page_number": common_data.get("page_number"),
        "covid19": common_data.get("covid19"),
        "topic": common_data.get("topic"),
        "scope": common_data.get("scope"),
        "space": common_data.get("space"),
        "equality_rights": common_data.get("equality_rights"),
        "about_women": common_data.get("about_women"),
        "inequality_women": common_data.get("inequality_women"),
        "stereotypes": common_data.get("stereotypes"),
        "comments": common_data.get("comments"),
        "further_analysis": common_data.get("further_analysis"),
    }


def get_data_for_radio(radio_coding_data, row):
    common_data = get_all_coding_data(radio_coding_data, row)

    return {
        "monitor_mode": common_data.get("monitor_mode"),
        "country": common_data.get("country"),
        "monitor_code": common_data.get("monitor_code"),
        "channel": common_data.get("channel"),
        "start_time": common_data.get("start_time"),
        "num_female_anchors": common_data.get("num_female_anchors"),
        "num_male_anchors": common_data.get("num_male_anchors"),
        "item_number": common_data.get("item_number"),
        "covid19": common_data.get("covid19"),
        "topic": common_data.get("topic"),
        "scope": common_data.get("scope"),
        "equality_rights": common_data.get("equality_rights"),
        "about_women": common_data.get("about_women"),
        "inequality_women": common_data.get("inequality_women"),
        "stereotypes": common_data.get("stereotypes"),
        "comments": common_data.get("comments"),
        "further_analysis": common_data.get("further_analysis"),
    }


def get_data_for_tv(tv_coding_data, row):
    common_data = get_all_coding_data(tv_coding_data, row)

    return {
        "monitor_mode": common_data.get("monitor_mode"),
        "country": common_data.get("country"),
        "monitor_code": common_data.get("monitor_code"),
        "channel": common_data.get("channel"),
        "start_time": common_data.get("start_time"),
        "num_female_anchors": common_data.get("num_female_anchors"),
        "num_male_anchors": common_data.get("num_male_anchors"),
        "item_number": common_data.get("item_number"),
        "covid19": common_data.get("covid19"),
        "topic": common_data.get("topic"),
        "scope": common_data.get("scope"),
        "equality_rights": common_data.get("equality_rights"),
        "about_women": common_data.get("about_women"),
        "inequality_women": common_data.get("inequality_women"),
        "stereotypes": common_data.get("stereotypes"),
        "comments": common_data.get("comments"),
        "further_analysis": common_data.get("further_analysis"),
    }


def get_data_for_internent_coding(internet_coding_data, row):
    common_data = get_all_coding_data(internet_coding_data, row)

    return {
        "monitor_mode": common_data.get("monitor_mode"),
        "country": common_data.get("country"),
        "monitor_code": common_data.get("monitor_code"),
        "website_name": common_data.get("website_name"),
        "website_url": common_data.get("website_url"),
        "time_accessed": common_data.get("time_accessed"),
        "offline_presence": common_data.get("offline_presence"),
        "webpage_layer_no": common_data.get("webpage_layer_no"),
        "covid19": common_data.get("covid19"),
        "topic": common_data.get("topic"),
        "scope": common_data.get("scope"),
        "shared_via_twitter": common_data.get("shared_via_twitter"),
        "shared_on_facebook": common_data.get("shared_on_facebook"),
        "equality_rights": common_data.get("equality_rights"),
        "about_women": common_data.get("about_women"),
        "inequality_women": common_data.get("inequality_women"),
        "stereotypes": common_data.get("stereotypes"),
        "url_and_multimedia": common_data.get("url_and_multimedia"),
        "further_analysis": common_data.get("further_analysis"),
    }


def get_data_for_twitter_coding(twitter_coding_data, row):
    common_data = get_all_coding_data(twitter_coding_data, row)

    return {
        "monitor_mode": common_data.get("monitor_mode"),
        "country": common_data.get("country"),
        "monitor_code": common_data.get("monitor_code"),
        "media_name": common_data.get("media_name"),
        "twitter_handle": common_data.get("twitter_handle"),
        "retweet": common_data.get("retweet"),
        "covid19": common_data.get("covid19"),
        "topic": common_data.get("topic"),
        "equality_rights": common_data.get("equality_rights"),
        "about_women": common_data.get("about_women"),
        "inequality_women": common_data.get("inequality_women"),
        "stereotypes": common_data.get("stereotypes"),
        "url_and_multimedia": common_data.get("url_and_multimedia"),
        "further_analysis": common_data.get("further_analysis"),
    }


def save_person_data(
    coding_data, person_data, row, serializer, country, sheet_name, sheet_tab
):
    person_data.update(get_people_data(coding_data, row))
    person_serialiser = serializer(data=person_data)
    if person_serialiser.is_valid():
        person_serialiser.save()
        ProcessedSheet.objects.create(
            country=country, sheet_name=sheet_name, sheet_tab=sheet_tab, sheet_row=row
        )
    else:
        UnProccessedRow.objects.get_or_create(
            country=country,
            sheet_name=sheet_name,
            sheet_tab=sheet_tab,
            sheet_row=row,
            row_error=person_serialiser.errors,
        )


def save_journalist_data(
    coding_data, row, serializer, sheet, parent_id, country, sheet_name, sheet_tab
):
    if coding_data:
        sex = coding_data.get("sex").get(row) if coding_data.get("sex") else None
        age = coding_data.get("age").get(row) if coding_data.get("age") else None
        journalist_data = {
            "sex": int(sex) if sex else None,
            "age": age,
            f"{sheet}": parent_id,
        }
        if sheet in ["television_sheet", "radio_sheet"]:
            journalist_data.update({"role": coding_data.get("role").get(row)})
        news_journalist_serializer = serializer(data=journalist_data)
        if news_journalist_serializer.is_valid():
            news_journalist_serializer.save()
            ProcessedSheet.objects.create(
                country=country,
                sheet_name=sheet_name,
                sheet_tab=sheet_tab,
                sheet_row=row,
            )
        else:
            UnProccessedRow.objects.get_or_create(
                country=country,
                sheet_name=sheet_name,
                sheet_tab=sheet_tab,
                sheet_row=row,
                row_error=news_journalist_serializer.errors,
            )


def save_newspaper_news_data(
    country, sheet_name, newspaper_coding_data, journalist_newspaper_coding_data
):
    if newspaper_coding_data:
        for row in newspaper_coding_data.get("story_label", []):

            sheet_data = get_data_for_newspaper_coding(newspaper_coding_data, row)
            newspaper_news_serializer = NewspaperSheetSerializer(data=sheet_data)

            if check_proccessed_row(country, sheet_name, "NewspaperCoding", row):
                # Let the user know we have processed this row
                print(
                    f"Row {row} of Sheet {sheet_name} in {country} has already been processed before"
                )
                continue

            if newspaper_news_serializer.is_valid():
                newspaper_news = newspaper_news_serializer.save()
                ProcessedSheet.objects.create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="NewspaperCoding",
                    sheet_row=row,
                )
                person_data = dict(newspaper_sheet=newspaper_news.id)
                person_row = row
                while has_person(newspaper_coding_data, person_row):
                    if check_proccessed_row(
                        country, sheet_name, "NewspaperCodingPerson", person_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {person_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_person_data(
                        newspaper_coding_data,
                        person_data,
                        person_row,
                        NewspaperPersonSerializer,
                        country,
                        sheet_name,
                        "NewspaperCodingPerson",
                    )
                    person_row = str(int(person_row) + 1)

                journalist_row = row
                while has_journalist(journalist_newspaper_coding_data, journalist_row):
                    if check_proccessed_row(
                        country, sheet_name, "NewspaperCodingJournalist", journalist_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {journalist_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_journalist_data(
                        journalist_newspaper_coding_data,
                        journalist_row,
                        NewspaperJournalistSerializer,
                        "newspaper_sheet",
                        newspaper_news.id,
                        country,
                        sheet_name,
                        "NewspaperCodingJournalist",
                    )
                    journalist_row = str(int(journalist_row) + 1)
            else:
                UnProccessedRow.objects.get_or_create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="NewspaperCoding",
                    sheet_row=row,
                    row_error=newspaper_news_serializer.errors,
                )


def save_radio_news_data(
    country, sheet_name, radio_coding_data, journalist_radio_coding_data
):
    if radio_coding_data:
        for row in radio_coding_data.get("story_label", []):

            sheet_data = get_data_for_radio(radio_coding_data, row)
            radio_news_serializer = RadioSheetSerializer(data=sheet_data)

            if check_proccessed_row(country, sheet_name, "RadioCoding", row):
                # Let the user know we have processed this row
                print(
                    f"Row {row} of Sheet {sheet_name} in {country} has already been processed before"
                )
                continue

            if radio_news_serializer.is_valid():
                radio_news = radio_news_serializer.save()
                ProcessedSheet.objects.create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="RadioCoding",
                    sheet_row=row,
                )
                person_data = dict(radio_sheet=radio_news.id)
                person_row = row
                while has_person(radio_coding_data, person_row):
                    if check_proccessed_row(
                        country, sheet_name, "RadioCodingPerson", person_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {person_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_person_data(
                        radio_coding_data,
                        person_data,
                        person_row,
                        RadioPersonSerializer,
                        country,
                        sheet_name,
                        "RadioCodingPerson",
                    )
                    person_row = str(int(person_row) + 1)

                journalist_row = row
                while has_journalist(journalist_radio_coding_data, journalist_row):
                    if check_proccessed_row(
                        country, sheet_name, "RadioCodingJournalist", journalist_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {journalist_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_journalist_data(
                        journalist_radio_coding_data,
                        journalist_row,
                        RadioJournalistSerializer,
                        "radio_sheet",
                        radio_news.id,
                        country,
                        sheet_name,
                        "RadioCodingJournalist",
                    )
                    journalist_row = str(int(journalist_row) + 1)
            else:
                UnProccessedRow.objects.get_or_create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="RadioCoding",
                    sheet_row=row,
                    row_error=radio_news_serializer.errors,
                )


def save_tv_news_data(country, sheet_name, tv_coding_data, journalist_tv_coding_data):
    if tv_coding_data:
        for row in tv_coding_data.get("story_label", []):

            sheet_data = get_data_for_tv(tv_coding_data, row)
            tv_news_serializer = TelevisionSheetSerializer(data=sheet_data)

            if check_proccessed_row(country, sheet_name, "TelevisionCoding", row):
                # Let the user know we have processed this row
                print(
                    f"Row {row} of Sheet {sheet_name} in {country} has already been processed before"
                )
                continue

            if tv_news_serializer.is_valid():
                tv_news = tv_news_serializer.save()
                ProcessedSheet.objects.create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="TelevisionCoding",
                    sheet_row=row,
                )
                person_data = dict(television_sheet=tv_news.id)
                person_row = row
                while has_person(tv_coding_data, person_row):
                    if check_proccessed_row(
                        country, sheet_name, "TelevisionCodingPerson", person_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {person_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_person_data(
                        tv_coding_data,
                        person_data,
                        person_row,
                        TelevisionPersonSerializer,
                        country,
                        sheet_name,
                        "TelevisionCodingPerson",
                    )
                    person_row = str(int(person_row) + 1)

                journalist_row = row
                while has_journalist(journalist_tv_coding_data, journalist_row):
                    if check_proccessed_row(
                        country,
                        sheet_name,
                        "TelevisionCodingJournalist",
                        journalist_row,
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {journalist_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_journalist_data(
                        journalist_tv_coding_data,
                        journalist_row,
                        TelevisionJournalistSerializer,
                        "television_sheet",
                        tv_news.id,
                        country,
                        sheet_name,
                        "TelevisionCodingJournalist",
                    )
                    journalist_row = str(int(journalist_row) + 1)
            else:
                UnProccessedRow.objects.get_or_create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="TelevisionCoding",
                    sheet_row=row,
                    row_error=tv_news_serializer.errors,
                )


def save_internent_news_data(
    country, sheet_name, internet_coding_data, journalist_internet_coding_data
):
    if internet_coding_data:
        for row in internet_coding_data.get("story_label", []):

            sheet_data = get_data_for_internent_coding(internet_coding_data, row)

            internet_news_sheet_serializer = InternetNewsSheetSerializer(
                data=sheet_data
            )
            if check_proccessed_row(country, sheet_name, "InternetCoding", row):
                # Let the user know we have processed this row
                print(
                    f"Row {row} of Sheet {sheet_name} in {country} has already been processed before"
                )
                continue

            if internet_news_sheet_serializer.is_valid():
                internet_news_sheet = internet_news_sheet_serializer.save()
                ProcessedSheet.objects.create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="InternetCoding",
                    sheet_row=row,
                )
                person_data = dict(internetnews_sheet=internet_news_sheet.id)
                # If next row is current row+1 then that row belongs to this sheet
                # e.g if current row is 2 and next row is 3 then that row holds the second Journalist or the second person in the news.
                person_row = row
                while has_person(internet_coding_data, person_row):
                    if check_proccessed_row(
                        country, sheet_name, "InternetCodingPerson", person_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {person_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_person_data(
                        internet_coding_data,
                        person_data,
                        person_row,
                        InternetNewsPersonSerializer,
                        country,
                        sheet_name,
                        "InternetCodingPerson",
                    )
                    person_row = str(int(person_row) + 1)

                journalist_row = row
                while has_journalist(journalist_internet_coding_data, journalist_row):
                    if check_proccessed_row(
                        country, sheet_name, "InternetCodingJournalist", journalist_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {journalist_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_journalist_data(
                        journalist_internet_coding_data,
                        journalist_row,
                        InternetNewsJournalistSerializer,
                        "internetnews_sheet",
                        internet_news_sheet.id,
                        country,
                        sheet_name,
                        "InternetCodingJournalist",
                    )
                    journalist_row = str(int(journalist_row) + 1)
            else:
                UnProccessedRow.objects.get_or_create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="InternetCoding",
                    sheet_row=row,
                    row_error=internet_news_sheet_serializer.errors,
                )


def save_twitter_news_data(
    country, sheet_name, twitter_coding_data, journalist_twitter_coding_data
):
    if twitter_coding_data:
        for row in twitter_coding_data.get("story_label", []):

            sheet_data = get_data_for_twitter_coding(twitter_coding_data, row)

            twitter_news_serializer = TwitterSheetSerializer(data=sheet_data)
            if check_proccessed_row(country, sheet_name, "TwitterCoding", row):
                # Let the user know we have processed this row
                print(
                    f"Row {row} of Sheet {sheet_name} in {country} has already been processed before"
                )
                continue

            if twitter_news_serializer.is_valid():
                twitter_news = twitter_news_serializer.save()
                ProcessedSheet.objects.create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="TwitterCoding",
                    sheet_row=row,
                )
                person_data = dict(twitter_sheet=twitter_news.id)
                person_row = row
                while has_person(twitter_coding_data, person_row):
                    if check_proccessed_row(
                        country, sheet_name, "TwitterCodingPerson", person_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {person_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_person_data(
                        twitter_coding_data,
                        person_data,
                        person_row,
                        TwitterPersonSerializer,
                        country,
                        sheet_name,
                        "TwitterCodingPerson",
                    )
                    person_row = str(int(person_row) + 1)

                journalist_row = row
                while has_journalist(journalist_twitter_coding_data, journalist_row):
                    if check_proccessed_row(
                        country, sheet_name, "TwitterCodingJournalist", journalist_row
                    ):
                        # Let the user know we have processed this row
                        print(
                            f"Row {journalist_row} of Sheet {sheet_name} in {country} has already been processed before"
                        )

                    save_journalist_data(
                        journalist_twitter_coding_data,
                        journalist_row,
                        TwitterJournalistSerializer,
                        "twitter_sheet",
                        twitter_news.id,
                        country,
                        sheet_name,
                        "TwitterCodingJournalist",
                    )

                    journalist_row = str(int(journalist_row) + 1)
            else:
                UnProccessedRow.objects.get_or_create(
                    country=country,
                    sheet_name=sheet_name,
                    sheet_tab="TwitterCoding",
                    sheet_row=row,
                    row_error=twitter_news_serializer.errors,
                )


def merge_data(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_data(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def get_common_coding_data(data):
    # This gives you data for the whole sheet. e.g {"countries": {row1, row2, row3, ..., rowN}}
    # You will thus be required to further extract data for individual rows while saving the data into the database
    # e.g .get('countries').get(row)
    if data:
        rows = [x for x in data["country_code"]]
        if not rows:
            return None
    else:
        return None
    # Ensure we only pick unique stories
    # This will remove story_labels with same value meaning same story
    story_label = {}
    for story in data["story_label"]:
        if not story_label.get(data["story_label"][story]):
            story_label.update({data["story_label"][story]: story})

    story_label = {y: x for x, y in story_label.items()}
    return {
        "countries": data.get("country_code"),
        "monitors": data.get("monitor_code"),
        "monitor_mode": data.get("monitor_mode"),
        "covid19": data.get("covid19"),
        "scope": data.get("scope"),
        "topic": data.get("topic"),
        "equality_rights": data.get("equality_rights"),
        "about_women": data.get("about_women"),
        "inequality_women": data.get("inequality_women"),
        "stereotypes": data.get("stereotypes"),
        "comments": data.get("comments"),
        "story_label": story_label,
        "sex": data.get("sex"),
        "age": data.get("age"),
        "occupation": data.get("occupation"),
        "function": data.get("function"),
        "family_role": data.get("family_role"),
        "victim_or_survivor": data.get("victim_or_survivor"),
        "victim_of": data.get("victim_of"),
        "survivor_of": data.get("survivor_of"),
        "is_quoted": data.get("is_quoted"),
        "is_photograph": data.get("is_photograph"),
        "special_qn_1": data.get("special_qn_1"),
        "special_qn_2": data.get("special_qn_2"),
        "special_qn_3": data.get("special_qn_3"),
        "further_analysis": data.get("further_analysis"),
    }


def get_newspaper_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []
    common_coding_data["newspaper_name"] = data.get("newspaper_name")
    common_coding_data["page_number"] = data.get("page_number")
    common_coding_data["space"] = data.get("space")

    return common_coding_data


def get_radio_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []
    common_coding_data["channel"] = data.get("channel")
    common_coding_data["start_time"] = data.get("start_time")
    common_coding_data["num_female_anchors"] = data.get("num_female_anchors")
    common_coding_data["num_male_anchors"] = data.get("num_male_anchors")
    common_coding_data["item_number"] = data.get("item_number")
    common_coding_data["role"] = data.get("role")

    return common_coding_data


def get_tv_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []

    common_coding_data["channel"] = data.get("channel")
    common_coding_data["start_time"] = data.get("start_time")
    common_coding_data["num_female_anchors"] = data.get("num_female_anchors")
    common_coding_data["num_male_anchors"] = data.get("num_male_anchors")
    common_coding_data["item_number"] = data.get("item_number")
    common_coding_data["role"] = data.get("role")

    return common_coding_data


def get_internet_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []

    common_coding_data["website_name"] = data.get("website_name")
    common_coding_data["website_url"] = data.get("website_url")
    common_coding_data["time_accessed"] = data.get("time_accessed")
    common_coding_data["offline_presence"] = data.get("offline_presence")
    common_coding_data["webpage_layer_no"] = data.get("webpage_layer_no")
    common_coding_data["shared_via_twitter"] = data.get("shared_via_twitter")
    common_coding_data["shared_on_facebook"] = data.get("shared_via_facebook")

    return common_coding_data


def get_twitter_coding_data(data):
    common_coding_data = get_common_coding_data(data)
    if not common_coding_data:
        return []
    common_coding_data["twitter_handle"] = data.get("twitter_handle")
    common_coding_data["retweet"] = data.get("retweet")
    common_coding_data["media_name"] = data.get("media_name")

    return common_coding_data


def format_date_time(date_time):
    return f"{date_time.year}-{date_time.month}-{date_time.day} {date_time.hour}:{date_time.minute}"


def format_time(time):
    timeformat = "%H.%M.%S"
    time = time.replace(":", ".")
    try:
        datetime.strptime(time, timeformat)
    except Exception:
        return "00:00:00"
    time = time.replace(".", ":")
    return time.strip()


def has_person(coding_data, row):
    if coding_data:
        if coding_data.get("sex") and coding_data.get("sex").get(row):
            return True
        elif coding_data.get("age") and coding_data.get("age").get(row):
            return True
        elif coding_data.get("occupation") and coding_data.get("occupation").get(row):
            return True
        elif coding_data.get("function") and coding_data.get("function").get(row):
            return True
        elif coding_data.get("family_role") and coding_data.get("family_role").get(row):
            return True
        elif coding_data.get("victim_or_survivor") and coding_data.get(
            "victim_or_survivor"
        ).get(row):
            return True
        elif coding_data.get("is_quoted") and coding_data.get("is_quoted").get(row):
            return True
        elif coding_data.get("is_photograph") and coding_data.get("is_photograph").get(
            row
        ):
            return True
        elif coding_data.get("special_qn_1") and coding_data.get("special_qn_1").get(
            row
        ):
            return True
        elif coding_data.get("special_qn_2") and coding_data.get("special_qn_2").get(
            row
        ):
            return True
        elif coding_data.get("special_qn_3") and coding_data.get("special_qn_3").get(
            row
        ):
            return True
        else:
            return False
    return False


def has_journalist(coding_data, row):
    if coding_data:
        if coding_data.get("sex") and coding_data.get("sex").get(row):
            return True
        elif coding_data.get("age") and coding_data.get("age").get(row):
            return True
        elif coding_data.get("role") and coding_data.get("role").get(row):
            return True
        else:
            return False
    return False


def yes_no(question):
    if question == "1":
        return "Y"
    elif question == "2":
        return "N"
    else:
        return None


def check_proccessed_row(country, sheet_name, sheet_tab, row):
    processed_sheet = ProcessedSheet.objects.filter(
        country=country, sheet_name=sheet_name, sheet_tab=sheet_tab, sheet_row=row
    ).first()
    return processed_sheet
