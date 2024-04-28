# gis/serializers.py

from rest_framework import serializers
from .models import GISMasterClass

class GISMasterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISMasterClass
        fields = '__all__'
