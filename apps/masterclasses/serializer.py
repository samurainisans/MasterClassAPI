# serializers.py
from rest_framework import serializers
from .models import Category, MasterClass, Participant, Speaker, Organizer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MasterClassSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    speakers = serializers.StringRelatedField(many=True)
    organizer_name = serializers.CharField(source='organizer.name', read_only=True)

    class Meta:
        model = MasterClass
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'
