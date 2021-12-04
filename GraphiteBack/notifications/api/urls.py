from django.urls import path, include
from rest_framework import routers

from notifications.api.views import NotificationViewSet

router = routers.SimpleRouter()

router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
