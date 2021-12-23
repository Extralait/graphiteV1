from PIL.Image import Image
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, PassportData


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        PassportData.objects.create(user=instance)
    if (created and instance.avatar) or (instance.tracker.has_changed('avatar') and instance.avatar):
        img = Image.open(instance.avatar.path)
        img.save(instance.avatar.path, "JPEG", quality=80, optimize=True, progressive=True)
    if (created and instance.cover) or (instance.tracker.has_changed('cover') and instance.cover):
        img = Image.open(instance.cover.path)
        img.save(instance.cover.path, "JPEG", quality=80, optimize=True, progressive=True)
