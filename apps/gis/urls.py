# gis/urls.py
from django.urls import path
from .views import GISMasterClassViewSet

urlpatterns = [
    path('geocode/', GISMasterClassViewSet.as_view({'get': 'geocode'}), name='gis-masterclass-geocode'),
]
