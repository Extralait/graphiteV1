from users.api.urls import urlpatterns as users
from drops.api.urls import urlpatterns as drops
from drops_collections.api.urls import urlpatterns as collections
from notifications.api.urls import urlpatterns as notifications
from offers.api.urls import urlpatterns as offers
from transactions.api.urls import urlpatterns as transactions
from auction.api.urls import urlpatterns as auction

urlpatterns = []
urlpatterns += users
urlpatterns += drops
urlpatterns += collections
urlpatterns += notifications
urlpatterns += offers
urlpatterns += transactions
urlpatterns += auction
