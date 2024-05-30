from rest_framework import viewsets
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass
from .serializer import MasterClassSerializer, CategorySerializer, UserMasterClassSerializer, FavoriteMasterClassSerializer

class MasterClassViewSet(viewsets.ModelViewSet):
    queryset = MasterClass.objects.all()
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
