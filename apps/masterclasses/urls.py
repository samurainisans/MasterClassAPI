# masterclasses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MasterClassViewSet, CategoryListView, ParticipantsListView, MasterClassParticipantsView

router = DefaultRouter()
router.register(r'', MasterClassViewSet, basename='masterclass')

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('<int:masterclass_id>/participants/', MasterClassParticipantsView.as_view(), name='masterclass-participants'),
    path('', include(router.urls)),
]
