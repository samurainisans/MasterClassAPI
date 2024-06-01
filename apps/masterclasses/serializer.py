# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/serializer.py
from rest_framework import serializers
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass, Participant
from ..users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'bio', 'image']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MasterClassSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()
    speaker = UserSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = MasterClass
        fields = '__all__'


class UserMasterClassSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserMasterClass
        fields = ['user', 'register_state', 'date_register']


class FavoriteMasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMasterClass
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Participant
        fields = ['user', 'registered_at']


class CitySerializer(serializers.Serializer):
    locality = serializers.CharField(max_length=255)