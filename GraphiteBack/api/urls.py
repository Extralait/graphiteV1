from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

# from api.views import RawFileViewSet,ProcessedFileViewSet

# Django REST framework routes
router = routers.DefaultRouter()
# router.register(r'row_files', RawFileViewSet)
# router.register(r'processed_files', ProcessedFileViewSet)

urlpatterns = [
    # DRF router
    path('', include(router.urls)),
    # djoser auth urls
    url(r'^auth/', include('djoser.urls')),
    # djoser auth jwt urls
    url(r'^auth/', include('djoser.urls.jwt')),
    # Логин GUI DRF
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
