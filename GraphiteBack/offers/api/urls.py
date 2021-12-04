from django.urls import path, include
from rest_framework import routers

from offers.api.views import OfferViewSet

router = routers.SimpleRouter()

router.register(r'offers', OfferViewSet)

urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
