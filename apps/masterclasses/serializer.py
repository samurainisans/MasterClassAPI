from rest_framework import serializers
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass, Participant
from ..users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class MasterClassCreateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    organizer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    speaker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MasterClass
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'duration', 'end_register_date',
            'categories', 'longitude', 'latitude', 'image_url', 'organizer', 'speaker', 'location_name',
            'country', 'province', 'area', 'locality', 'street', 'house', 'postal_code', 'requires_approval',
            'price'
        ]


class MasterClassUpdateSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    organizer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    speaker = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = MasterClass
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'duration', 'end_register_date',
            'categories', 'longitude', 'latitude', 'image_url', 'organizer', 'speaker', 'location_name',
            'country', 'province', 'area', 'locality', 'street', 'house', 'postal_code', 'requires_approval',
            'price'
        ]
        read_only_fields = ['id']


class MasterClassSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()
    speaker = UserSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = MasterClass
        fields = [
            'id', 'title', 'description', 'start_date', 'end_date', 'duration', 'end_register_date',
            'categories', 'longitude', 'latitude', 'image_url', 'organizer', 'speaker', 'location_name',
            'country', 'province', 'area', 'locality', 'street', 'house', 'postal_code', 'requires_approval',
            'price'
        ]



class UserMasterClassSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserMasterClass
        fields = ['user', 'register_state', 'date_register']


class FavoriteMasterClassSerializer(serializers.ModelSerializer):
    master_class = MasterClassSerializer()

    class Meta:
        model = FavoriteMasterClass
        fields = ['id', 'user', 'master_class']


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Participant
        fields = ['user', 'registered_at']


class CitySerializer(serializers.Serializer):
    locality = serializers.CharField(max_length=255)
