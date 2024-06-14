# C:/Users/Nik/Desktop/DjangoBackendMasterclases/MasterClassAPI/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('apps.chat.urls')),
    path('api/masterclasses/', include('apps.masterclasses.urls')),
    path('api/gis/', include('apps.gis.urls')),
    # path('api/users/', include('apps.users.urls')),
    path('', include('apps.users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
