import json
import json
import logging

from django.db.models import JSONField
from django.contrib import admin
from django.forms import widgets

from django.contrib import admin

from drops.models import SpecialCollectionDrop, Drop
from drops_collections.models import SpecialCollection
from utils.admin import PaginationInline


class DropsInline(PaginationInline):
    model = SpecialCollectionDrop
    autocomplete_fields = ['collection', 'drop']
    search_fields = ['collection__name', 'drop__name']
    extra = 1


@admin.register(SpecialCollection)
class SpecialCollectionAdmin(admin.ModelAdmin):
    inlines = [DropsInline]
    search_fields = ['name']


class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            return super(PrettyJSONWidget, self).format_value(value)


class JsonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }


@admin.register(Drop)
class DropAdmin(JsonAdmin):

    autocomplete_fields = ['artist', 'owner', 'from_collection', 'parent']
    search_fields = ['name']
    list_filter = ['blockchain_type','sell_type','to_sell','is_active','category']

    list_display = ['name', 'picture_small_tag', 'category', 'all_count', 'in_stock', 'sell_count']

    fieldsets = (
        ('Blockchain', {'fields': ('blockchain_type', 'blockchain_address', 'blockchain_identifier')}),
        ('About drop', {'fields': ('name', 'descriptions','category','tags','specifications')}),
        ('Relations', {'fields': ('artist', 'owner', 'parent','from_collection','level')}),
        ('Sell settings', {'fields': ('sell_type','sell_count','in_stock',
                                      'all_count','init_cost','min_rate',
                                      'royalty','auction_deadline','to_sell',)}),
        ('Media content', {
            'fields': ('url_landing',('picture_small_tag','picture_small'),('picture_big_tag','picture_big'),('color','color_tag')),
        }),
        ('Hronology', {
            'fields': ('created_at', 'updated_at'),
        }),
        ('Permissions', {
            'fields': ('is_active',),
        }),
    )

    readonly_fields = ['created_at', 'updated_at','picture_small_tag','picture_big_tag','color_tag']

    def specifications(self, instance):
        data = json.loads(instance.specifications)
        return data["specifications"]
