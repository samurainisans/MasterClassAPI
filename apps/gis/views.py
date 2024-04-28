# gis/views.py

from rest_framework import viewsets
from .models import GISMasterClass
from .serializer import GISMasterClassSerializer


class GISMasterClassViewSet(viewsets.ModelViewSet):
    queryset = GISMasterClass.objects.all()
    serializer_class = GISMasterClassSerializer
