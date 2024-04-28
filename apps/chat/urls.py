# chat/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.chat import views

router = DefaultRouter()
router.register(r'send-messages', views.SendMessagesViewSet, basename='my-messages')
urlpatterns = [
    path('get-messages/<sender_id>/<reciever_id>/', views.GetMessages.as_view()),
    path('', include(router.urls)),
]
