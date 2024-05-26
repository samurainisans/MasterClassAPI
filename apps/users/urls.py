# users/urls.py
from django.urls import path, include
from apps.users.views import UserRegistrationAPIView, UserLoginAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('', include(router.urls)),
]
