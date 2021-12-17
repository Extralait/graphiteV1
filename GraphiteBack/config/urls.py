from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings
from users.api import urls


urlpatterns = [
    # Панель администратора
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    # API для приложений
    path("api/v1/", include("config.api.v1",)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.DOCUMENTATION_URL, document_root=settings.DOCUMENTATION_ROOT)
