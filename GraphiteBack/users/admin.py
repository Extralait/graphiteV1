from django.contrib import admin

from drops.models import DropSubscription, DropLike, DropView
from drops_collections.models import CollectionSubscription, CollectionLike, CollectionView
from notifications.models import Notification
from offers.models import Offer
from transactions.models import Transaction
from users.models import User, PassportData, UsersGroup, UsersGroupUser, UserSubscription, UserView
from utils.admin import PaginationInline


class UsersInline(PaginationInline):
    model = UsersGroupUser
    extra = 1
    autocomplete_fields = ['user_group','user']
    search_fields = ['user_group','user']


@admin.register(UsersGroup)
class UsersGroupAdmin(admin.ModelAdmin):
    inlines = (UsersInline,)
    search_fields = ['name']


class UserSubscriptionsInline(PaginationInline):
    model = UserSubscription
    extra = 1
    fk_name = 'subscription'
    autocomplete_fields = ['subscriber', 'subscription']
    search_fields = ['subscriber', 'subscription']


class DropSubscriptionsInline(PaginationInline):
    model = DropSubscription
    extra = 1
    autocomplete_fields = ['user', 'drop']
    search_fields = ['user', 'drop']


class CollectionSubscriptionsInline(PaginationInline):
    model = CollectionSubscription
    extra = 1
    autocomplete_fields = ['user', 'collection']
    search_fields = ['user', 'collection']


class DropLikesInline(PaginationInline):
    model = DropLike
    extra = 1
    autocomplete_fields = ['user', 'drop']
    search_fields = ['user', 'drop']


class CollectionsLikesInline(PaginationInline):
    model = CollectionLike
    extra = 1
    autocomplete_fields = ['user', 'collection']
    search_fields = ['user', 'collection']


class UserViewsInline(PaginationInline):
    fk_name = 'overlooked'
    model = UserView
    extra = 1
    autocomplete_fields = ['overlooked', 'looking']
    search_fields = ['overlooked', 'looking']


class DropViewsInline(PaginationInline):
    model = DropView
    extra = 1
    autocomplete_fields = ['user', 'drop']
    search_fields = ['user', 'drop']


class CollectionViewsInline(PaginationInline):
    model = CollectionView
    extra = 1
    autocomplete_fields = ['user', 'collection']
    search_fields = ['user', 'collection']


class PassportDataInline(admin.StackedInline):
    model = PassportData
    inline_type = 'stacked'
    autocomplete_fields = ['owner']
    search_fields = ['owner']


class FromYouNotificationInline(PaginationInline):
    model = Notification
    inline_type = 'tabular'
    fk_name = 'from_user'
    autocomplete_fields = ['to_user','from_user','to_drop','to_collection']
    search_fields = ['to_user','from_user','to_drop','to_collection']


class ToYouNotificationInline(PaginationInline):
    model = Notification
    inline_type = 'tabular'
    fk_name = 'to_user'
    autocomplete_fields = ['to_user','from_user','to_drop','to_collection']
    search_fields = ['to_user','from_user','to_drop','to_collection']


class ToYouUserOfferInline(PaginationInline):
    model = Offer
    inline_type = 'tabular'
    fk_name = 'owner'
    autocomplete_fields = ['owner','buyer','drop']
    search_fields = ['owner','buyer','drop']


class FromYouUserOfferInline(PaginationInline):
    model = Offer
    inline_type = 'tabular'
    fk_name = 'buyer'
    autocomplete_fields = ['owner','buyer','drop']
    search_fields = ['owner','buyer','drop']


class FromYouTransactionInline(PaginationInline):
    model = Transaction
    inline_type = 'tabular'
    fk_name = 'buyer'
    autocomplete_fields = ['owner','buyer','drop']
    search_fields = ['owner','buyer','drop']


class ToYouTransactionInline(PaginationInline):
    model = Transaction
    inline_type = 'tabular'
    fk_name = 'owner'
    autocomplete_fields = ['owner','buyer','drop']
    search_fields = ['owner','buyer','drop']


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



