# URL Configuration
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('apps.chat.urls')),
    path('masterclasses/', include('apps.masterclasses.urls')),
    path('users/', include('apps.users.urls')),
]
