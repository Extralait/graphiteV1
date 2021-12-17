from drops_collections.models import Collection

from django.contrib import admin




@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['owner']
    search_fields = ['owner']
