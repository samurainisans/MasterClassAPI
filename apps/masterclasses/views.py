# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/views.py
import django_filters
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass, Participant
from .serializer import MasterClassSerializer, CategorySerializer, UserMasterClassSerializer, \
    FavoriteMasterClassSerializer, ParticipantSerializer, CitySerializer, MasterClassCreateSerializer


class MasterClassPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(cache_page(60 * 15), name='dispatch')
class UserMasterClassViewSet(viewsets.ModelViewSet):
    queryset = UserMasterClass.objects.select_related('user', 'master_class')
    serializer_class = UserMasterClassSerializer


@method_decorator(cache_page(60 * 15), name='dispatch')
class FavoriteMasterClassViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMasterClass.objects.select_related('user', 'master_class')
    serializer_class = FavoriteMasterClassSerializer


@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(cache_page(60 * 15), name='dispatch')
class ParticipantsListView(generics.ListAPIView):
    queryset = Participant.objects.select_related('user', 'master_class')
    serializer_class = ParticipantSerializer


class MasterClassParticipantsView(generics.ListAPIView):
    serializer_class = UserMasterClassSerializer

    def get_queryset(self):
        masterclass_id = self.kwargs['masterclass_id']
        return UserMasterClass.objects.filter(master_class_id=masterclass_id).select_related('user', 'master_class')


@method_decorator(cache_page(60 * 15), name='dispatch')
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


@method_decorator(cache_page(60 * 15), name='list')  # кеширование на 15 минут
class MasterClassViewSet(viewsets.ModelViewSet):
    queryset = MasterClass.objects.annotate(participant_count=Count('participants')).select_related('organizer',
                                                                                                    'speaker').prefetch_related(
        'categories')
    serializer_class = MasterClassSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MasterClassFilter
    search_fields = ['title']
    pagination_class = MasterClassPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return MasterClassCreateSerializer
        return MasterClassSerializer
