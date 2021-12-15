from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from auction.api.views import AuctionUserBidViewSet, AuctionViewSet

router = ExtendedSimpleRouter()
# Аукционы
auctions_router = router.register(
    prefix=r'auctions',
    viewset=AuctionViewSet,
    basename='auction'
)
(
    # Подписчики на дроп
    auctions_router.register(
        prefix=r'bids',
        viewset=AuctionUserBidViewSet,
        parents_query_lookups=['auction'],
        basename='auction-bids'
    ),
)
router.register(
    prefix=r'bids',
    viewset=AuctionUserBidViewSet,
    basename='bids'
)
urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
