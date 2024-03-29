"""User models admin."""


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cride.users.models import User, Profile


class CustomUserAdmin(UserAdmin):
    """User model admin."""
    list_display = ("email", "username", "first_name", "last_name", "is_staff", "is_client")
    list_filter = ("is_client", "is_staff", "created", "modified")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ("user", "reputation", "rides_offereed", "rides_taken")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    list_fields = ("reputation",)


admin.site.register(User, CustomUserAdmin)
