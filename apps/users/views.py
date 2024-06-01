# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/views.py
from rest_framework import viewsets
from .models import User, Role, Contact
from .serializer import UserSerializer, RoleSerializer, ContactSerializer
from ..masterclasses.models import Category, FavoriteMasterClass
from ..masterclasses.serializer import CategorySerializer, FavoriteMasterClassSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMasterClass.objects.all()
    serializer_class = FavoriteMasterClassSerializer

