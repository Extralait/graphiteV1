from django.contrib import admin

from drops.models import SpecialCollectionDrop, Drop
from drops_collections.models import SpecialCollection


class DropsInline(admin.TabularInline):
    model = SpecialCollectionDrop
    extra = 1


@admin.register(SpecialCollection)
class SpecialCollectionAdmin(admin.ModelAdmin):
    inlines = [DropsInline]


@admin.register(Drop)
class DropAdmin(admin.ModelAdmin):
    pass
