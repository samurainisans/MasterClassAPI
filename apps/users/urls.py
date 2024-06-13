# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PasswordResetView, PasswordResetConfirmView, UserRegistrationView, ActivateView, \
    RoleViewSet, SpeakerViewSet, UserLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('roles/', RoleViewSet.as_view({'get': 'list'}), name='roles-list'),
    path('speakers/', SpeakerViewSet.as_view({'get': 'list'}), name='speakers-list'),
    path('organizers/', UserViewSet.as_view({'get': 'list'}), name='organizers-list'),

    path('', include(router.urls)),
]
