#  C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/views.py
import django_filters
from rest_framework import viewsets, generics
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass, Participant
from .serializer import MasterClassSerializer, CategorySerializer, UserMasterClassSerializer, \
    FavoriteMasterClassSerializer, ParticipantSerializer, CitySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# class MasterClassViewSet(viewsets.ModelViewSet):
#     queryset = MasterClass.objects.select_related('organizer', 'speaker').prefetch_related('categories')
#     serializer_class = MasterClassSerializer


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


class CitiesListView(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        return [{'locality': locality} for locality in
                MasterClass.objects.values_list('locality', flat=True).distinct()]


class MasterClassFilter(django_filters.FilterSet):
    categories = django_filters.AllValuesMultipleFilter(field_name='categories__id')
    locality = django_filters.AllValuesMultipleFilter(field_name='locality')
    start_date = django_filters.DateTimeFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='end_date', lookup_expr='lte')

    class Meta:
        model = MasterClass
        fields = ['categories', 'locality', 'start_date', 'end_date']

class MasterClassViewSet(viewsets.ModelViewSet):
    queryset = MasterClass.objects.select_related('organizer', 'speaker').prefetch_related('categories')
    serializer_class = MasterClassSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MasterClassFilter