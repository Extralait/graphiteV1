from django.conf.urls import url
from django.urls import path, include
from rest_framework_extensions.routers import ExtendedSimpleRouter

from drops.api.views import DropViewSet
from drops_collections.api.views import CollectionViewSet
from notifications.api.views import NotificationViewSet
from offers.api.views import OfferViewSet
from transactions.api.views import TransactionViewSet
from users.api.views import UserProfileViewSet

router = ExtendedSimpleRouter()

# Профиль пользователя
users_profiles_router = router.register(
    prefix=r'users-profiles',
    viewset=UserProfileViewSet,
    basename='users-profiles'
)
(
    # Уведомдения пользователя
    users_profiles_router.register(
        prefix=r'notices',
        viewset=NotificationViewSet,
        parents_query_lookups=['to_user'],
        basename='users-profiles-notices'
    ),
    # Транзакции продажи
    users_profiles_router.register(
        prefix=r'sell-transactions',
        viewset=TransactionViewSet,
        parents_query_lookups=['owner'],
        basename='users-profiles-sell-transactions'
    ),
    # Транзакции покупки
    users_profiles_router.register(
        prefix=r'buy-transactions',
        viewset=TransactionViewSet,
        parents_query_lookups=['buyer'],
        basename='users-profiles-buy-transactions'
    ),
    # Предложения продажа
    users_profiles_router.register(
        prefix=r'sell-offers',
        viewset=OfferViewSet,
        parents_query_lookups=['owner'],
        basename='users-profiles-sell-offers'
    ),
    # Предложения покупка
    users_profiles_router.register(
        prefix=r'buy-offers',
        viewset=OfferViewSet,
        parents_query_lookups=['buyer'],
        basename='users-profiles-buy-offers'
    ),
    # Коллекции во владении пользователя
    users_profiles_router.register(
        prefix=r'collections',
        viewset=CollectionViewSet,
        parents_query_lookups=['owner'],
        basename='users-profiles-collections'
    ).register(
        prefix=r'drops',
        viewset=DropViewSet,
        parents_query_lookups=['from_collection__owner','from_collection' ],
        basename='users-profiles-collection-drops'
    ),
    # Подписки пользователя на пользователей
    users_profiles_router.register(
        prefix=r'profile-subscriptions',
        viewset=UserProfileViewSet,
        parents_query_lookups=['user_subscriptions'],
        basename='users-profiles-profile-subscriptions'
    ),
    # Подписки пользователя на дроп
    users_profiles_router.register(
        prefix=r'drop-subscriptions',
        viewset=DropViewSet,
        parents_query_lookups=['drop_subscriptions'],
        basename='users-profiles-drop-subscriptions'
    ),
    # Подписки пользователя на коллекции
    users_profiles_router.register(
        prefix=r'collection-subscriptions',
        viewset=CollectionViewSet,
        parents_query_lookups=['collection_subscriptions'],
        basename='users-profiles-collection-subscriptions'
    ),
    # Подписки на пользователя
    users_profiles_router.register(
        prefix=r'profile-subscribers',
        viewset=UserProfileViewSet,
        parents_query_lookups=['subscribers'],
        basename='users-profiles-profile-subscribers'
    ),
    # Просмотры пользователя
    users_profiles_router.register(
        prefix=r'views',
        viewset=UserProfileViewSet,
        parents_query_lookups=['views'],
        basename='users-profiles-views'
    ),
    # Дропы во владении пользователя
    users_profiles_router.register(
        prefix=r'drops',
        viewset=DropViewSet,
        parents_query_lookups=['owner'],
        basename='users-profiles-drops'
    ),
)


urlpatterns = [
    # djoser auth jwt urls
    url(r'^auth/', include('djoser.urls.jwt')),
    # DRF router
    path('', include(router.urls)),
    # DRF GUI login
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
