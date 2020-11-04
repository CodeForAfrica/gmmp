from rest_framework import serializers

from forms.models import (
            NewspaperSheet, NewspaperPerson, NewspaperJournalist,
            InternetNewsSheet, InternetNewsPerson, InternetNewsJournalist,
)

class NewspaperSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewspaperSheet
        fields = '__all__'
        read_only_fields = ['id']

class NewspaperPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewspaperPerson
        fields = '__all__'
        read_only_fields = ['id']

class NewspaperJournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewspaperJournalist
        fields = '__all__'
        read_only_fields = ['id']

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

