"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CrideModel


class User(CrideModel, AbstractUser):


    email = models.EmailField(
        help_text="email address",
        unique=True,
        error_messages={
            "unique": "A user with that email already exists"
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$'
    )

    phone_number = models.CharField(max_length=17, blank=True, validators=[phone_regex])

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    is_client = models.BooleanField(
        "client",
        default=True,
        help_text=(
            "Help easily distinguish users and perform queries."
            "Clients are the main type of users"),
    )

    is_verified = models.BooleanField(
        "verified",
        default=True,
        help_text="Set to true when the user have verified its email address."
    )

    def __str__(self) -> str:
        return self.username

    def get_short_name(self):
        return self.username