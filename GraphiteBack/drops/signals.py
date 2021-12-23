from io import StringIO

from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from auction.models import Auction
from auction.services.auction_operations import auction_waiter
from drops.models import Drop
from drops.services.color_converter import find_closest_color
from utils.parsers import get_aware_datetime


@receiver(post_save, sender=Drop)
def post_save_drop(sender, instance, created, **kwargs):
    to_sell = instance.to_sell
    sell_type = instance.sell_type
    if to_sell and not instance.tracker.previous('to_sell') and sell_type == 'auction':
        auction = Auction.objects.create(drop=instance)
        auction_waiter.apply_async([auction.pk],
                                   countdown=(get_aware_datetime(instance.auction_deadline) - now()).total_seconds())

    if (created and instance.picture_big) or (instance.tracker.has_changed('picture_big') and instance.picture_big):
        find_closest_color.delay(instance.pk, instance.picture_big.path)
    if (created and instance.picture_small) or (instance.tracker.has_changed('picture_small') and instance.picture_small):
        img = Image.open(instance.picture_small.path)
        img.save(instance.picture_small.path, "JPEG", quality=80, optimize=True, progressive=True)
    if (created and instance.picture_big) or (instance.tracker.has_changed('picture_big') and instance.picture_big):
        img = Image.open(instance.picture_big.path)
        img.save(instance.picture_big.path, "JPEG", quality=80, optimize=True, progressive=True)
