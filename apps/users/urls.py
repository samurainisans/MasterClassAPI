# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,  FavoriteViewSet, UserRegistrationView, ActivateView, RoleViewSet

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='user')
router.register(r'api/roles', RoleViewSet, basename='role')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('', include(router.urls)),
]
