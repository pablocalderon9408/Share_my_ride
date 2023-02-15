"""Circles URLs."""

# Django
from django.urls import path

# Views
from cride.users.views import login_view

urlpatterns = [
    path('users/login', login_view, name='login'),
]
