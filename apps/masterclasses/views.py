# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/views.py

import django_filters
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass, Participant
from .serializer import MasterClassSerializer, CategorySerializer, UserMasterClassSerializer, \
    FavoriteMasterClassSerializer, ParticipantSerializer, CitySerializer, MasterClassCreateSerializer, MasterClassUpdateSerializer
from ..users.models import User

class MasterClassPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@method_decorator(cache_page(60 * 15), name='dispatch')
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class UserMasterClassViewSet(viewsets.ModelViewSet):
    queryset = UserMasterClass.objects.select_related('user', 'master_class')
    serializer_class = UserMasterClassSerializer


class FavoriteMasterClassViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMasterClass.objects.all()
    serializer_class = FavoriteMasterClassSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='add')
    def add_favorite(self, request):
        user = request.user
        master_class_id = request.data.get('master_class_id')
        try:
            master_class = MasterClass.objects.get(id=master_class_id)
        except MasterClass.DoesNotExist:
            return Response({'status': 'master class not found'}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = FavoriteMasterClass.objects.get_or_create(user=user, master_class=master_class)
        if created:
            return Response({'status': 'master class added to favorites'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'master class already in favorites'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_favorite(self, request):
        user = request.user
        master_class_id = request.data.get('master_class_id')
        try:
            favorite = FavoriteMasterClass.objects.get(user=user, master_class_id=master_class_id)
            favorite.delete()
            return Response({'status': 'master class removed from favorites'}, status=status.HTTP_200_OK)
        except FavoriteMasterClass.DoesNotExist:
            return Response({'status': 'favorite master class not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='my')
    def my_favorites(self, request):
        user = request.user
        favorites = FavoriteMasterClass.objects.filter(user=user)
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)


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
        elif self.action in ['update', 'partial_update']:
            return MasterClassUpdateSerializer
        return MasterClassSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.role.name not in ['Admin', 'Organizer']:
            return Response({'status': 'permission denied'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({'status': 'master class deleted'}, status=status.HTTP_204_NO_CONTENT)
