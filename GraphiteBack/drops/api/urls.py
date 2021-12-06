from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from drops.api.views import DropViewSet, CategoryViewSet, TagViewSet
from offers.api.views import OfferViewSet
from transactions.api.views import TransactionViewSet
from users.api.views import UserProfileViewSet

router = ExtendedSimpleRouter()
# Коллекции
drops_router = router.register(
    prefix=r'drops',
    viewset=DropViewSet,
    basename='drops'
)
(
    # Подписчики на дроп
    drops_router.register(
        prefix=r'subscribers',
        viewset=UserProfileViewSet,
        parents_query_lookups=['drop_subscriptions'],
        basename='drops-subscribers'
    ),
    # Лайки на дроп
    drops_router.register(
        prefix=r'likes',
        viewset=UserProfileViewSet,
        parents_query_lookups=['drop_likes'],
        basename='drops-likes'
    ),
    # Просмотры дропа
    drops_router.register(
        prefix=r'views',
        viewset=UserProfileViewSet,
        parents_query_lookups=['drop_views'],
        basename='drops-views'
    ),
    # Транзакции продажи
    drops_router.register(
        prefix=r'sell-transactions',
        viewset=TransactionViewSet,
        parents_query_lookups=['drop'],
        basename='drops-sell-transactions'
    ),
    # Транзакции покупки
    drops_router.register(
        prefix=r'buy-transactions',
        viewset=TransactionViewSet,
        parents_query_lookups=['drop'],
        basename='drops-buy-transactions'
    ),
    # Предложения продажа
    drops_router.register(
        prefix=r'sell-offers',
        viewset=OfferViewSet,
        parents_query_lookups=['drop'],
        basename='drops-sell-offers'
    ),
    # Предложения покупка
    drops_router.register(
        prefix=r'buy-offers',
        viewset=OfferViewSet,
        parents_query_lookups=['drop'],
        basename='drops-buy-offers'
    ),
)
router.register(
    prefix=r'drops-tags',
    viewset=TagViewSet,
    basename='drops-tags'
)
router.register(
    prefix=r'drops-categories',
    viewset=CategoryViewSet,
    basename='drops-categories'
)
urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
