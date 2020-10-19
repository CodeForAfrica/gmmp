from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import (
    NewspaperSheet,
    RadioSheet,
    TelevisionSheet,
    InternetNewsSheet,
    TwitterSheet
)

# Create your views here.
class DataUploadEndpoint(APIView):
    def get(self, request):
        newspapers = NewspaperSheet.objects.all();
        print(newspapers, flush=True)
        Response({"message": "Get some data!",})

    def post(self, request):
        """
            Upload data sent as JSON
        """
        for data in request.data:
            self._create(data['data'], data['type'])

        return Response({"message": "Post some data!",})

    def _create(self, data, type):
        """
            Create objects in database
        """
        types = dict(
            newspaper=self._newspaper_creator,
            radio=self._radio_creator,
            television=self._television_creator,
            internet=self._internet_creator,
            twitter=self._twitter_creator
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
        return NewspaperSheet.objects.create(
            newspaper_name=data.get('newspaperName', ""),
            page_number=data.get('pageNumber', ""),
            covid19=data.get('covid19', ""),
            topic=data.get('topic', ""),
            scope=data.get('scope', ""),
            space=data.get('space', ""),
            equality_rights=data.get('equalityRights', ""),
            about_women=data.get('aboutWomen', ""),
            inequality_women=data.get('inequalityWomen', ""),
            stereotypes=data.get('stereotypes', ""),
            further_analysis=data.get('furtherAnalysis', ""),
            comments=data.get('comments', ""),
            country=data.get('country', ""),
        )

    def _radio_creator(self, data):
        """
            Create radio sheet in database
        """
        return RadioSheet.objects.create(
            channel=data.get('channel', ""),
            start_time=data.get('startTime', ""),
            num_female_anchors=data.get('numFemaleAnchors', ""),
            num_male_anchors=data.get('numMaleAnchors', ""),
            item_number=data.get('itemNumber', ""),
            covid19=data.get('covid19', ""),
            topic=data.get('topic', ""),
            scope=data.get('spascopece', ""),
            equality_rights=data.get('equalityRights', ""),
            about_women=data.get('aboutWomen', ""),
            inequality_women=data.get('inequalityWomen', ""),
            stereotypes=data.get('stereotypes', ""),
            further_analysis=data.get('furtherAnalysis', ""),
            comments=data.get('comments', ""),
            country=data.get('country', ""),
        )

    def _television_creator(self, data):
        """
            Create television sheet in database
        """
        return TelevisionSheet.objects.create(
            channel=data.get('channel', ""),
            start_time=data.get('startTime', ""),
            num_female_anchors=data.get('numFemaleAnchors', ""),
            num_male_anchors=data.get('numMaleAnchors', ""),
            item_number=data.get('itemNumber', ""),
            covid19=data.get('covid19', ""),
            topic=data.get('topic', ""),
            scope=data.get('spascopece', ""),
            equality_rights=data.get('equalityRights', ""),
            about_women=data.get('aboutWomen', ""),
            inequality_women=data.get('inequalityWomen', ""),
            stereotypes=data.get('stereotypes', ""),
            further_analysis=data.get('furtherAnalysis', ""),
            comments=data.get('comments', ""),
            country=data.get('country', ""),
        )

    def _internet_creator(self, data):
        """
            Create internet sheet in database
        """
        return InternetNewsSheet.objects.create(
            website_name=data.get('websiteName', ""),
            website_url=data.get('websiteUrl', ""),
            time_accessed=data.get('timeAccessed', ""),
            offline_presence=data.get('offlinePresence', ""),
            webpage_layer_no=data.get('webpageLayerNo', ""),
            covid19=data.get('covid19', ""),
            topic=data.get('topic', ""),
            scope=data.get('scope', ""),
            shared_via_twitter=data.get('sharedViaTwitter', ""),
            shared_on_facebook=data.get('sharedOnFacebook', ""),
            equality_rights=data.get('equalityRights', ""),
            about_women=data.get('aboutWomen', ""),
            inequality_women=data.get('inequalityWomen', ""),
            stereotypes=data.get('stereotypes', ""),
            further_analysis=data.get('furtherAnalysis', ""),
            url_and_multimedia=data.get('urlAndMultimedia', ""),
            country=data.get('country', ""),
        )

    def _twitter_creator(self, data):
        """
            Create twitter sheet in database
        """
        return TwitterSheet.objects.create(
            media_name=data.get('mediaName', ""),
            twitter_handle=data.get('twitterHandle', ""),
            retweet=data.get('retweet', ""),
            covid19=data.get('covid19', ""),
            topic=data.get('topic', ""),
            equality_rights=data.get('equalityRights', ""),
            about_women=data.get('aboutWomen', ""),
            inequality_women=data.get('inequalityWomen', ""),
            stereotypes=data.get('stereotypes', ""),
            further_analysis=data.get('furtherAnalysis', ""),
            url_and_multimedia=data.get('urlAndMultimedia', ""),
            country=data.get('country', ""),
        )
