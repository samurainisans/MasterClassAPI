# masterclasses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'masterclasses', views.MasterClassViewSet, basename='masterclasses')
router.register(r'participants', views.ParticipantViewSet, basename='participants')
router.register(r'speakers', views.SpeakerViewSet, basename='speakers')
router.register(r'organizers', views.OrganizerViewSet, basename='organizers')

urlpatterns = [
    path('', include(router.urls)),
]
