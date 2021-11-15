from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from api.views import UserProfileViewSet, CategoriesViewSet, TagsViewSet, DropViewSet, UserUserSubscriptionViewSet, \
    UserDropSubscriptionViewSet, DropLikeViewSet, BuyDrop, OwnerDropViewSet, DropViewViewSet, CollectionViewSet, \
    UserCollectionSubscriptionViewSet, OwnerCollectionViewSet, CollectionLikeViewSet, CollectionViewViewSet, \
    CollectionDropViewSet

# Django REST framework routes
router = routers.DefaultRouter()
router.register(r'users-profiles', UserProfileViewSet)
router.register(r'users-subscriptions', UserUserSubscriptionViewSet)

router.register(r'drops', DropViewSet)
router.register(r'drop-categories', CategoriesViewSet)
router.register(r'drop-tags', TagsViewSet)
router.register(r'drops-owners', OwnerDropViewSet)
router.register(r'drops-subscriptions', UserDropSubscriptionViewSet)
router.register(r'drops-likes', DropLikeViewSet)
router.register(r'drops-views', DropViewViewSet)

router.register(r'collections', CollectionViewSet)
router.register(r'collections-owners', OwnerCollectionViewSet)
router.register(r'collections-drops', CollectionDropViewSet)
router.register(r'collections-subscriptions', UserCollectionSubscriptionViewSet)
router.register(r'collections-likes', CollectionLikeViewSet)
router.register(r'collections-views', CollectionViewViewSet)

urlpatterns = [
    # djoser auth urls
    url(r'^auth/', include('djoser.urls')),
    # djoser auth jwt urls
    url(r'^auth/', include('djoser.urls.jwt')),
    # DRF router
    path('', include(router.urls)),
    # DRF no router paths
    path('buy-drop/', BuyDrop.as_view()),
    # Логин GUI DRF
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
