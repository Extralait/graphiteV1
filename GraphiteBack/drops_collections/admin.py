from drops_collections.models import Collection

from django.contrib import admin




@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass