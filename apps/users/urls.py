# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,  FavoriteViewSet
from ..masterclasses.views import ParticipantsListView

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = [
    path('participants/', ParticipantsListView.as_view()),
    # path('favorites/', FavoriteViewSet.as_view()),
    path('', include(router.urls)),
]
