from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from auction.models import Auction
from auction.services.auction_operations import auction_waiter
from drops.models import Drop
from utils.parsers import get_aware_datetime


@receiver(post_save, sender=Drop)
def post_save_drop(sender, instance, created, **kwargs):
    to_sell = instance.to_sell
    sell_type = instance.sell_type
    if to_sell and not instance.tracker.previous('to_sell') and sell_type == 'auction':
        auction = Auction.objects.create(drop=instance)
        auction_waiter.apply_async([auction.pk],countdown=(get_aware_datetime(instance.auction_deadline)-now()).total_seconds())
