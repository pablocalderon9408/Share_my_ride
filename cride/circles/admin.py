"""Circle models admin."""


from django.contrib import admin

from cride.circles.models import Circle


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ("name", "slug_name", "rides_offered", "rides_taken", "is_public", "verified")
    search_fields = ("name", "slug_name")
