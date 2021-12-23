import json

from drops.admin import JsonAdmin
from drops_collections.models import Collection

from django.contrib import admin


@admin.register(Collection)
class CollectionAdmin(JsonAdmin):
    autocomplete_fields = ['owner']
    search_fields = ['owner']

    list_display = ['name', 'picture_small_tag']

    fieldsets = (
        ('About collection', {'fields': ('name','specifications')}),
        ('Relations', {'fields': ('owner',)}),
        ('Media content', {
            'fields': (('picture_small_tag','picture_small'),('picture_big_tag','picture_big')),
        }),
        ('Hronology', {
            'fields': ('created_at', 'updated_at'),
        }),
        ('Permissions', {
            'fields': ('is_active',),
        }),
    )

    readonly_fields = ['created_at', 'updated_at','picture_small_tag','picture_big_tag']

    def specifications(self, instance):
        data = json.loads(instance.specifications)
        return data["specifications"]
