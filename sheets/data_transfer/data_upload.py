from forms.models import (
    NewspaperSheet,
    RadioSheet,
    TelevisionSheet,
    InternetNewsSheet,
    TwitterSheet,
    InternetNewsPerson,
    InternetNewsJournalist,
    TwitterJournalist,
    TwitterPerson,
    TelevisionJournalist,
    TelevisionPerson,
    RadioPerson,
    RadioJournalist,
    NewspaperPerson,
    NewspaperJournalist,
)
from .index import merge_coded_data

# Create your views here.


class DataUpload():
    def post(self):
        """
            Upload data
        """
        sheet_name, coding = 'bbc_world', 'InternetCoding'
        data = merge_coded_data(sheet_name, coding)
        for item in data:
            self._create(item, coding)

    def _create(self, data, type):
        """
            Create objects in database
        """
        types = dict(
            NewspaperCoding=self._newspaper_creator,
            RadioCoding=self._radio_creator,
            TelevisionCoding=self._television_creator,
            InternetCoding=self._internet_creator,
            TwitterCodings=self._twitter_creator
        )
        for item in data:
            try:
                types.get(type, self._newspaper_creator)(item)
            except BaseException as e:
                print(f'exception happened = {str(e)}')

    def _newspaper_creator(self, data):
        """
            Create newspaper sheet in database
        """
        newspaper_sheet = NewspaperSheet.objects.create(
            newspaper_name=data.get('newspaper_name'),
            page_number=data.get('page_number'),
            covid19=data.get('covid19'),
            topic=data.get('topic'),
            scope=data.get('scope'),
            space=data.get('space'),
            equality_rights=data.get('equality_rights'),
            about_women=data.get('about_women'),
            inequality_women=data.get('inequality_women'),
            stereotypes=data.get('stereotypes'),
            further_analysis=data.get('further_analysis'),
            comments=data.get('comments'),
            country=data.get('country'),
        )
        for person in data['people']:
            NewspaperPerson.objects.create(
                sex=person.get("sex"),
                age=person.get("age"),
                occupation=person.get("occupation"),
                function=person.get("function"),
                family_role=person.get("family_role"),
                victim_or_survivor=person.get("victim_or_survivor"),
                victim_of=person.get("victim_of"),
                survivor_of=person.get("survivor_of"),
                is_quoted=person.get("is_quoted"),
                is_photograph=person.get("is_photograph"),
                special_qn_1=person.get("special_qn_1"),
                special_qn_2=person.get("special_qn_2"),
                special_qn_3=person.get("special_qn_3"),
                newspaper_sheet=newspaper_sheet
            )

        for journalist in data['journalists']:
            NewspaperJournalist.objects.create(
                newspaper_sheet=newspaper_sheet,
                sex=journalist.get("sex"),
                age=journalist.get("age"),
            )

    def _radio_creator(self, data):
        """
            Create radio sheet in database
        """
        radio_sheet = RadioSheet.objects.create(
            channel=data.get('channel'),
            start_time=data.get('start_time'),
            num_female_anchors=data.get('num_female_anchors'),
            num_male_anchors=data.get('num_male_anchors'),
            item_number=data.get('item_number'),
            covid19=data.get('covid19'),
            topic=data.get('topic'),
            scope=data.get('spascopece'),
            equality_rights=data.get('equality_rights'),
            about_women=data.get('about_women'),
            inequality_women=data.get('inequality_women'),
            stereotypes=data.get('stereotypes'),
            further_analysis=data.get('further_analysis'),
            comments=data.get('comments'),
            country=data.get('country'),
        )
        for person in data['people']:
            RadioPerson.objects.create(
                sex=person.get("sex"),
                occupation=person.get("occupation"),
                function=person.get("function"),
                family_role=person.get("family_role"),
                victim_or_survivor=person.get("victim_or_survivor"),
                victim_of=person.get("victim_of"),
                survivor_of=person.get("survivor_of"),
                special_qn_1=person.get("special_qn_1"),
                special_qn_2=person.get("special_qn_2"),
                special_qn_3=person.get("special_qn_3"),
                radio_sheet=radio_sheet
            )

        for journalist in data['journalists']:
            RadioJournalist.objects.create(
                radio_sheet=radio_sheet,
                sex=journalist.get("sex"),
                age=journalist.get("age"),
            )

    def _television_creator(self, data):
        """
            Create television sheet in database
        """
        television_sheet = TelevisionSheet.objects.create(
            channel=data.get('channel'),
            start_time=data.get('start_time'),
            num_female_anchors=data.get('num_female_anchors'),
            num_male_anchors=data.get('num_male_anchors'),
            item_number=data.get('item_number'),
            covid19=data.get('covid19'),
            topic=data.get('topic'),
            scope=data.get('spascopece'),
            equality_rights=data.get('equality_rights'),
            about_women=data.get('about_women'),
            inequality_women=data.get('inequality_women'),
            stereotypes=data.get('stereotypes'),
            further_analysis=data.get('further_analysis'),
            comments=data.get('comments'),
            country=data.get('country'),
        )
        for person in data['people']:
            TelevisionPerson.objects.create(
                sex=person.get("sex"),
                age=person.get("age"),
                occupation=person.get("occupation"),
                function=person.get("function"),
                family_role=person.get("family_role"),
                victim_or_survivor=person.get("victim_or_survivor"),
                victim_of=person.get("victim_of"),
                survivor_of=person.get("survivor_of"),
                special_qn_1=person.get("special_qn_1"),
                special_qn_2=person.get("special_qn_2"),
                special_qn_3=person.get("special_qn_3"),
                television_sheet=television_sheet
            )

        for journalist in data['journalists']:
            TelevisionJournalist.objects.create(
                television_sheet=television_sheet,
                sex=journalist.get("sex"),
                age=journalist.get("age"),
                role=journalist.get("role")
            )

    def _internet_creator(self, data):
        """
            Create internet sheet in database
        """
        internet_news = InternetNewsSheet.objects.create(
            website_name=data.get('website_name'),
            website_url=data.get('website_url'),
            time_accessed=data.get('time_accessed'),
            offline_presence=data.get('offline_presence'),
            webpage_layer_no=data.get('webpage_layer_no'),
            covid19=data.get('covid19'),
            topic=data.get('topic'),
            scope=data.get('scope'),
            shared_via_twitter=data.get('shared_via_twitter'),
            shared_on_facebook=data.get('shared_via_facebook'),
            equality_rights=data.get('equality_rights'),
            about_women=data.get('about_women'),
            inequality_women=data.get('inequality_women'),
            stereotypes=data.get('stereotypes'),
            further_analysis=data.get('further_analysis'),
            url_and_multimedia=data.get('url_and_multimedia'),
            country=data.get('country'),
        )
        for person in data['people']:
            InternetNewsPerson.objects.create(
                sex=person.get("sex"),
                age=person.get("age"),
                occupation=person.get("occupation"),
                function=person.get("function"),
                family_role=person.get("family_role"),
                victim_or_survivor=person.get("victim_or_survivor"),
                victim_of=person.get("victim_of"),
                survivor_of=person.get("survivor_of"),
                is_quoted=person.get("is_quoted"),
                is_photograph=person.get("is_photograph"),
                special_qn_1=person.get("special_qn_1"),
                special_qn_2=person.get("special_qn_2"),
                special_qn_3=person.get("special_qn_3"),
                internetnews_sheet=internet_news
            )

        for journalist in data['journalists']:
            InternetNewsJournalist.objects.create(
                internetnews_sheet=internet_news,
                sex=journalist.get("sex"),
                age=journalist.get("age")
            )

    def _twitter_creator(self, data):
        """
            Create twitter sheet in database
        """
        twitter_news = TwitterSheet.objects.create(
            media_name=data.get('media_name'),
            twitter_handle=data.get('twitter_handle'),
            retweet=data.get('retweet'),
            covid19=data.get('covid19'),
            topic=data.get('topic'),
            equality_rights=data.get('equality_rights'),
            about_women=data.get('about_women'),
            inequality_women=data.get('inequality_women'),
            stereotypes=data.get('stereotypes'),
            further_analysis=data.get('further_analysis'),
            url_and_multimedia=data.get('url_and_multimedia'),
            country=data.get('country'),
        )
        for person in data['people']:
            TwitterPerson.objects.create(
                sex=person.get("sex"),
                age=person.get("age"),
                occupation=person.get("occupation"),
                function=person.get("function"),
                is_photograph=person.get("is_photograph"),
                special_qn_1=person.get("special_qn_1"),
                special_qn_2=person.get("special_qn_2"),
                special_qn_3=person.get("special_qn_3"),
                twitter_sheet=twitter_news
            )

        for journalist in data['journalists']:
            TwitterJournalist.objects.create(
                twitter_sheet=twitter_news,
                sex=journalist.get("sex"),
                age=journalist.get("age")
            )
