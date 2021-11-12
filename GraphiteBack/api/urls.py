from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from api.views import UserProfileViewSet, CategoriesViewSet, TagsViewSet, DropViewSet, UserUserSubscriptionViewSet, \
    UserDropSubscriptionViewSet, LikeViewSet

# Django REST framework routes
router = routers.DefaultRouter()
router.register(r'users-profiles', UserProfileViewSet)
router.register(r'drop-categories', CategoriesViewSet)
router.register(r'drop-tags', TagsViewSet)
router.register(r'drops', DropViewSet)
router.register(r'users-subscriptions', UserUserSubscriptionViewSet)
router.register(r'drops-subscriptions', UserDropSubscriptionViewSet)
router.register(r'likes', LikeViewSet)

urlpatterns = [
    # djoser auth urls
    url(r'^auth/', include('djoser.urls')),
    # djoser auth jwt urls
    url(r'^auth/', include('djoser.urls.jwt')),
    # DRF router
    path('', include(router.urls)),
    # Логин GUI DRF
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
