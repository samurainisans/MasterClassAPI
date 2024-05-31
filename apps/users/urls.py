# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

