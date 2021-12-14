from django.contrib import admin

# Register your models here.
from django.contrib.admin.options import InlineModelAdmin

from drops.models import SpecialCollectionDrop, DropSubscription, DropLike, DropView
from drops_collections.models import CollectionSubscription, CollectionLike, CollectionView
from notifications.models import Notification
from offers.models import Offer
from transactions.models import Transaction
from users.models import User, PassportData, UsersGroup, UsersGroupUser, UserSubscription, UserView


# admin.site.register(User)
# admin.site.register(PassportData)


class UsersInline(admin.TabularInline):
    model = UsersGroupUser
    extra = 1


class UsersGroupAdmin(admin.ModelAdmin):
    inlines = (UsersInline,)


admin.site.register(UsersGroup, UsersGroupAdmin)


class UserSubscriptionsInline(admin.TabularInline):
    model = UserSubscription
    extra = 1
    fk_name = 'subscription'


class DropSubscriptionsInline(admin.TabularInline):
    model = DropSubscription
    extra = 1


class CollectionSubscriptionsInline(admin.TabularInline):
    model = CollectionSubscription
    extra = 1


class DropLikesInline(admin.TabularInline):
    model = DropLike
    extra = 1


class CollectionsLikesInline(admin.TabularInline):
    model = CollectionLike
    extra = 1


class UserViewsInline(admin.TabularInline):
    fk_name = 'overlooked'
    model = UserView
    extra = 1


class DropViewsInline(admin.TabularInline):
    model = DropView
    extra = 1


class CollectionViewsInline(admin.TabularInline):
    model = CollectionView
    extra = 1


class PassportDataInline(admin.StackedInline):
    model = PassportData
    inline_type = 'stacked'


class FromYouNotificationInline(admin.TabularInline):
    model = Notification
    inline_type = 'tabular'
    fk_name = 'from_user'


class ToYouNotificationInline(admin.TabularInline):
    model = Notification
    inline_type = 'tabular'
    fk_name = 'to_user'


class ToYouUserOfferInline(admin.TabularInline):
    model = Offer
    inline_type = 'tabular'
    fk_name = 'owner'


class FromYouUserOfferInline(admin.TabularInline):
    model = Offer
    inline_type = 'tabular'
    fk_name = 'buyer'


class FromYouTransactionInline(admin.TabularInline):
    model = Transaction
    inline_type = 'tabular'
    fk_name = 'buyer'


class ToYouTransactionInline(admin.TabularInline):
    model = Transaction
    inline_type = 'tabular'
    fk_name = 'owner'


@admin.register(User)
class UserInlinesAdmin(admin.ModelAdmin):
    inlines = [UserSubscriptionsInline, UserViewsInline,
               DropSubscriptionsInline, DropLikesInline, DropViewsInline,
               CollectionSubscriptionsInline, CollectionsLikesInline,
               CollectionViewsInline, FromYouNotificationInline, ToYouNotificationInline, ToYouUserOfferInline,
               FromYouUserOfferInline, FromYouTransactionInline, ToYouTransactionInline]

    list_display = ['wallet_number', 'avatar_tag', 'first_name', 'last_name', 'profile_type', 'verify_status']
    search_fields = ['wallet_number', 'first_name', 'last_name', 'profile_type', 'verify_status', 'is_active']
    ordering = ['wallet_number']

    fieldsets = (
        (None, {'fields': ('wallet_number', 'owner_key', 'password')}),
        ('Personal info', {'fields': (('first_name', 'last_name'), 'inn')}),
        ('About profile', {'fields': ('profile_type', 'description','balance')}),
        ('Personal contacts', {'fields': ('email', 'instagram', 'twitter', 'tiktok',
                                          'discord', 'telegram', 'website')}),
        ('Media content', {'fields': (('avatar_tag','avatar'), ('cover_tag','cover'))}),
        ('Hronology', {
            'fields': ('date_joined', 'updated_at', 'last_login'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser','email_notification',
                       'verify_status', 'groups', 'user_permissions'),
        }),
    )

    readonly_fields = ['date_joined', 'updated_at', 'last_login','avatar_tag','cover_tag']



