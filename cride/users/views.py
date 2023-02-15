"""Users views."""

# Django
from django.http import HttpResponse


def login_view(request):
    """Login view."""
    return HttpResponse('Hello World')
