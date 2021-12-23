from django.core.management.base import BaseCommand

from drops.models import Drop
from drops.services.color_converter import find_closest_color


class Command(BaseCommand):
    help = 'Fill db'  # Описание команды

    def handle(self, *args, **kwargs):
        for i,drop in enumerate(Drop.objects.all()):
            # try:
            find_closest_color.delay(drop.pk, drop.picture_big.path)
            # except:
            #     pass
            print(i, drop.pk)

