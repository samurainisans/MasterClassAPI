# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/masterclasses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MasterClassViewSet, CategoryListView, MasterClassParticipantsView, CitiesListView, \
    FavoriteMasterClassViewSet, UserMasterClassViewSet

router = DefaultRouter()
router.register(r'', MasterClassViewSet, basename='masterclass')
router.register(r'favorites', FavoriteMasterClassViewSet, basename='favorite-masterclass')

urlpatterns = [
    path('cities/', CitiesListView.as_view(), name='cities-list'),
    path('categories/', CategoryListView.as_view(), name='categories-list'),
    path('<int:masterclass_id>/participants/', MasterClassParticipantsView.as_view(), name='masterclass-participants'),
    path('', include(router.urls)),
]