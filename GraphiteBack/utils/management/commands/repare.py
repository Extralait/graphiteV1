import logging
import os
from bulk_update.helper import bulk_update

import datetime
from django.core.management.base import BaseCommand
import random
import string
import json

from django.utils.timezone import now
from lorem import get_paragraph

from auction.services.auction_operations import place_bid
from drops.models import Drop, Tag, Category
from drops.services.like import add_like as add_drop_like
from drops.services.subscription import add_subscription as add_drop_subscription
from drops.services.view import add_view as add_drop_view
from drops_collections.services.like import add_like as add_collection_like
from drops_collections.services.subscription import add_subscription as add_collection_subscription
from drops_collections.services.view import add_view as add_collection_view
from drops_collections.models import Collection
from offers.services.offer_operations import make_offer
from transactions.services.transaction_operations import buy_drop
from users.models import User
from config.settings import MEDIA_ROOT
from users.services.subscription import add_subscription as add_user_subscription
from users.services.view import add_view as add_user_view





class Command(BaseCommand):
    help = 'Fill db'  # Описание команды

    def handle(self, *args, **kwargs):
        for i,drop in enumerate(Drop.objects.all()):
            if str(drop.picture_big).startswith('/'):
                drop.picture_big = str(drop.picture_big)[1:]
                drop.save()
                print(i, drop.pk)
