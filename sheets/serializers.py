from rest_framework import serializers

from forms.models import (
    NewspaperSheet,
    NewspaperPerson,
    NewspaperJournalist,
    InternetNewsSheet,
    InternetNewsPerson,
    InternetNewsJournalist,
    RadioSheet,
    RadioPerson,
    RadioJournalist,
    TelevisionPerson,
    TelevisionJournalist,
    TelevisionSheet,
    TwitterJournalist,
    TwitterPerson,
    TwitterSheet,
)


class TwitterSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterSheet
        fields = '__all__'
        read_only_fields = ['id']

class TwitterPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterPerson
        fields = '__all__'
        read_only_fields = ['id']


class TwitterJournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterJournalist
        fields = '__all__'
        read_only_fields = ['id']
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


class RadioSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioSheet
        fields = '__all__'
        read_only_fields = ['id']

class RadioPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioPerson
        fields = '__all__'
        read_only_fields = ['id']

class RadioJournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioJournalist
        fields = '__all__'
        read_only_fields = ['id']


class TelevisionSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelevisionSheet
        fields = '__all__'
        read_only_fields = ['id']

class TelevisionPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelevisionPerson
        fields = '__all__'
        read_only_fields = ['id']

class TelevisionJournalistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelevisionJournalist
        fields = '__all__'
        read_only_fields = ['id']