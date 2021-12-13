from django.contrib import admin
from django.contrib import admin

# Register your models here.
from users.models import User, PassportData, UsersGroup, UsersGroupUser

admin.site.register(User)
admin.site.register(PassportData)


class UsersInline(admin.TabularInline):
    model = UsersGroupUser
    extra = 1


class UsersGroupAdmin(admin.ModelAdmin):
    inlines = (UsersInline,)


admin.site.register(UsersGroup, UsersGroupAdmin)
