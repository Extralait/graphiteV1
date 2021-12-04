from django.conf.urls.static import static
# from django.contrib import admin
from django.urls import path, include

from config import settings
from users.api import urls

urlpatterns = [
    # Второй стиль админки
    path('grappelli/', include('grappelli.urls')),
    # Панель администратора
    # path('admin/', admin.site.urls),
    # API для приложений
    path("api/v1/", include("config.api.v1",)),
    # path("api/", include("drops.api.urls")),
    # path("api/", include("drops_collections.api.urls")),
    # path("api/", include("notifications.api.urls")),
    # path("api/", include("transactions.api.urls")),
    # path("api/", include("offers.api.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.DOCUMENTATION_URL, document_root=settings.DOCUMENTATION_ROOT)
