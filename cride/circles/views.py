"""Circles views."""

# Django
from django.http import HttpResponse

# Models
from cride.circles.models import Circle


def list_circles(request):
    """List circles."""
    circles = Circle.objects.filter(is_public=True)
    data = []
    for circle in circles:
        data.append({
            'name': circle.name,
            'slug_name': circle.slug_name,
            'rides_taken': circle.rides_taken,
            'rides_offered': circle.rides_offered,
            'members_limit': circle.members_limit
        })
    return HttpResponse(data, status=200)
