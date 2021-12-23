from PIL.Image import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

from drops_collections.models import Collection


@receiver(post_save, sender=Collection)
def post_save_collection(sender, instance, created, **kwargs):
    if (created and instance.picture_small) or (
            instance.tracker.has_changed('picture_small') and instance.picture_small):
        img = Image.open(instance.picture_small.path)
        img.save(instance.picture_small.path, "JPEG", quality=80, optimize=True, progressive=True)
    if (created and instance.picture_big) or (instance.tracker.has_changed('picture_big') and instance.picture_big):
        img = Image.open(instance.picture_big.path)
        img.save(instance.picture_big.path, "JPEG", quality=80, optimize=True, progressive=True)
