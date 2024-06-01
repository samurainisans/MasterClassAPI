# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/views.py

from rest_framework import viewsets

from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass
from .serializer import MasterClassSerializer, CategorySerializer, UserMasterClassSerializer, \
    FavoriteMasterClassSerializer


class MasterClassViewSet(viewsets.ModelViewSet):
    queryset = MasterClass.objects.select_related('organizer', 'speaker').prefetch_related('categories')
    serializer_class = MasterClassSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserMasterClassViewSet(viewsets.ModelViewSet):
    queryset = UserMasterClass.objects.all()
    serializer_class = UserMasterClassSerializer

class FavoriteMasterClassViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMasterClass.objects.all()
    serializer_class = FavoriteMasterClassSerializer
