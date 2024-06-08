from django.contrib import admin

from apps.user.models import User, Friends, FriendRequest


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    pass


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
