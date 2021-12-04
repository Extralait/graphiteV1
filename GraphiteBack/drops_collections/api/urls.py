from os.path import basename

from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from drops.api.views import DropViewSet
from drops_collections.api.views import CollectionViewSet, SpecialCollectionViewSet
from users.api.views import UserProfileViewSet

router = ExtendedSimpleRouter()
# Коллекции
collections_router = router.register(
    prefix=r'collections',
    viewset=CollectionViewSet,
    basename='collections'
)
(
    # Подписчики на колекцию
    collections_router.register(
        prefix=r'subscribers',
        viewset=UserProfileViewSet,
        parents_query_lookups=['collection_subscriptions'],
        basename='collection-subscribers'
    ),
    # Лайки на колекции
    collections_router.register(
        prefix=r'likes',
        viewset=UserProfileViewSet,
        parents_query_lookups=['collection_likes'],
        basename='collection-likes'
    ),
    # Просмотры колекции
    collections_router.register(
        prefix=r'views',
        viewset=UserProfileViewSet,
        parents_query_lookups=['collection_views'],
        basename='collection-views'
    ),
    # Дропы
    collections_router.register(
        prefix=r'drops',
        viewset=DropViewSet,
        parents_query_lookups=['from_collection'],
        basename='collection-drops'
    ),
)
router.register(
    prefix=r'special-collections',
    viewset=SpecialCollectionViewSet,
    basename='special-collections'
)

urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
