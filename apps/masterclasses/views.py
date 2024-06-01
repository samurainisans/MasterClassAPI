#  C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/views.py
from rest_framework import viewsets, generics
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass, Participant
from .serializer import MasterClassSerializer, CategorySerializer, UserMasterClassSerializer, \
    FavoriteMasterClassSerializer, ParticipantSerializer


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


class MasterClassListView(generics.ListAPIView):
    queryset = MasterClass.objects.all()
    serializer_class = MasterClassSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ParticipantsListView(generics.ListAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class MasterClassParticipantsView(generics.ListAPIView):
    serializer_class = UserMasterClassSerializer

    def get_queryset(self):
        masterclass_id = self.kwargs['masterclass_id']
        return UserMasterClass.objects.filter(master_class_id=masterclass_id)
