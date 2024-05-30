from rest_framework import serializers
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass

class MasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClass
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class UserMasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMasterClass
        fields = '__all__'

class FavoriteMasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMasterClass
        fields = '__all__'
