# gis/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GISMasterClassViewSet

router = DefaultRouter()
router.register(r'data', GISMasterClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-coordinates/', GISMasterClassViewSet.as_view({'post': 'update_coordinates'}),
         name='update-coordinates'),
]
