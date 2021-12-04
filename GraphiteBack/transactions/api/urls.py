from django.urls import path, include
from rest_framework import routers

from transactions.api.views import TransactionViewSet

router = routers.SimpleRouter()

router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
