from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.static import serve

from Config import settings

urlpatterns = [
                  path('grappelli/', include('grappelli.urls')),  # Второй стиль админки
                  path('admin/', admin.site.urls),
                  path("api/", include("api.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
