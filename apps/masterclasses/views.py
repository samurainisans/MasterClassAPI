# masterclasses/views.py
import logging

import django_filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import MasterClass, Category, UserMasterClass, FavoriteMasterClass, Participant
from .serializer import MasterClassSerializer, CategorySerializer, UserMasterClassSerializer, \
    FavoriteMasterClassSerializer, ParticipantSerializer, CitySerializer, MasterClassCreateSerializer, \
    MasterClassUpdateSerializer
from ..users.models import User

logger = logging.getLogger(__name__)


class MasterClassPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@method_decorator(cache_page(60 * 5), name='dispatch')
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
        master_class = get_object_or_404(MasterClass, id=master_class_id)

        favorite, created = FavoriteMasterClass.objects.get_or_create(user=user, master_class=master_class)
        if created:
            return Response({'status': 'favorite added', 'detail': 'Master class added to favorites.'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'already favorite', 'detail': 'Master class already in favorites.'},
                            status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='remove')
    def remove_favorite(self, request):
        user = request.user
        master_class_id = request.data.get('master_class_id')
        favorite = get_object_or_404(FavoriteMasterClass, user=user, master_class_id=master_class_id)

        favorite.delete()
        return Response({'status': 'favorite removed', 'detail': 'Master class removed from favorites.'},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my')
    def my_favorites(self, request):
        user = request.user
        favorites = FavoriteMasterClass.objects.filter(user=user)
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)


@method_decorator(cache_page(60 * 5), name='dispatch')
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ParticipantsListView(generics.ListAPIView):
    queryset = Participant.objects.select_related('user', 'master_class')
    serializer_class = ParticipantSerializer


class MasterClassParticipantsView(generics.ListAPIView):
    serializer_class = UserMasterClassSerializer

    def get_queryset(self):
        masterclass_id = self.kwargs['masterclass_id']
        return UserMasterClass.objects.filter(master_class_id=masterclass_id).select_related('user', 'master_class')


@method_decorator(cache_page(60 * 5), name='dispatch')
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


@method_decorator(cache_page(60 * 5), name='list')
class MasterClassViewSet(viewsets.ModelViewSet):
    queryset = MasterClass.objects.annotate(participant_count=Count('participants')).select_related('organizer',
                                                                                                    'speaker').prefetch_related(
        'categories')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = MasterClassFilter
    search_fields = ['title']
    pagination_class = MasterClassPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_serializer_class(self):
        if self.action == 'create':
            return MasterClassCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return MasterClassUpdateSerializer
        return MasterClassSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        required_permission = 'masterclasses.delete_masterclass'

        # Проверка, имеет ли пользователь необходимое разрешение
        if not user.has_perm(required_permission):
            return Response(
                {'status': 'permission denied', 'detail': 'You do not have permission to delete this masterclass.'},
                status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response({'status': 'master class deleted'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='register', permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        user = request.user
        try:
            master_class = MasterClass.objects.get(pk=pk)
        except MasterClass.DoesNotExist:
            return Response({'status': 'not found', 'detail': 'Master class not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        if UserMasterClass.objects.filter(user=user, master_class=master_class).exists():
            return Response(
                {'status': 'already registered', 'detail': 'You are already registered for this masterclass.'},
                status=status.HTTP_400_BAD_REQUEST)

        if master_class.requires_approval:
            UserMasterClass.objects.create(user=user, master_class=master_class, register_state='pending')
            return Response({'status': 'registration pending', 'detail': 'Registration is pending approval.'},
                            status=status.HTTP_201_CREATED)
        else:
            UserMasterClass.objects.create(user=user, master_class=master_class, register_state='accepted')
            return Response({'status': 'registration successful', 'detail': 'Registration successful.'},
                            status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='confirm_registration', permission_classes=[IsAuthenticated])
    def confirm_registration(self, request, pk=None):
        organizer = request.user
        if not organizer.role.name in ['Admin', 'Organizer']:
            return Response(
                {'status': 'permission denied', 'detail': 'You do not have permission to confirm registrations.'},
                status=status.HTTP_403_FORBIDDEN)

        user_masterclass_id = request.data.get('user_masterclass_id')
        new_state = request.data.get('new_state')

        if new_state not in ['accepted', 'rejected']:
            return Response({'status': 'invalid state', 'detail': 'Invalid state provided.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user_masterclass = UserMasterClass.objects.get(pk=user_masterclass_id, master_class_id=pk)
        except UserMasterClass.DoesNotExist:
            return Response({'status': 'not found', 'detail': 'Registration not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        user_masterclass.register_state = new_state
        user_masterclass.save()

        return Response({'status': f'registration {new_state}', 'detail': f'Registration has been {new_state}.'},
                        status=status.HTTP_200_OK)

