# gis/urls.py
from django.urls import path
from .views import GISMasterClassViewSet

urlpatterns = [
    path('geocode/', GISMasterClassViewSet.as_view({'get': 'geocode'}), name='gis-masterclass-geocode'),
    path('reverse-geocode/', GISMasterClassViewSet.as_view({'get': 'reverse_geocode'}),
         name='gis-masterclass-reverse-geocode'),
]
