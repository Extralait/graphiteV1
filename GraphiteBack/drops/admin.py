from django.contrib import admin

from drops_collections.models import SpecialCollection
from drops.models import SpecialCollectionDrop


class DropsInline(admin.TabularInline):
    model = SpecialCollectionDrop
    extra = 1


class SpecialCollectionAdmin(admin.ModelAdmin):
    inlines = (DropsInline,)


admin.site.register(SpecialCollection, SpecialCollectionAdmin)
