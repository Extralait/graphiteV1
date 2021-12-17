from django.contrib import admin

from drops.models import SpecialCollectionDrop, Drop
from drops_collections.models import SpecialCollection
from utils.admin import PaginationInline


class DropsInline(PaginationInline):
    model = SpecialCollectionDrop
    autocomplete_fields = ['collection', 'drop']
    search_fields = ['collection', 'drop']
    extra = 1


@admin.register(SpecialCollection)
class SpecialCollectionAdmin(admin.ModelAdmin):
    inlines = [DropsInline]
    search_fields = ['name']


@admin.register(Drop)
class DropAdmin(admin.ModelAdmin):
    autocomplete_fields = ['artist', 'owner','from_collection','parent']
    search_fields = ['artist', 'owner','from_collection','parent']
