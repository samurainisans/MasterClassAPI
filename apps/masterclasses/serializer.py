# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/serializer.py
from rest_framework import serializers
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass
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
    class Meta:
        model = UserMasterClass
        fields = '__all__'

class FavoriteMasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMasterClass
        fields = '__all__'
