from rest_framework import serializers

from forms.models import InternetNewsSheet, InternetNewsPerson, InternetNewsJournalist

class InternetNewsSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternetNewsSheet
        fields = '__all__'
        read_only_fields = ['id']

class InternetNewsPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternetNewsPerson
        fields = '__all__'
        read_only_fields = ['id']

class InternetNewsJournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternetNewsJournalist
        fields = '__all__'
        read_only_fields = ['id']

