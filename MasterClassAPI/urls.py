# URL Configuration
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('apps.chat.urls')),
    path('masterclasses/', include('apps.masterclasses.urls')),
    path('gis/', include('apps.gis.urls')),
    path('users/', include('apps.users.urls')),
]
