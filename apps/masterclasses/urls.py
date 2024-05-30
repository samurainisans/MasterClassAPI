from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MasterClassViewSet, CategoryViewSet, UserMasterClassViewSet, FavoriteMasterClassViewSet

router = DefaultRouter()
router.register(r'masterclasses', MasterClassViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'usermasterclasses', UserMasterClassViewSet)
router.register(r'favoritemasterclasses', FavoriteMasterClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
