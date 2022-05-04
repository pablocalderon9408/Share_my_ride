"""Profile Model."""

from distutils.command.upload import upload
from tokenize import blank_re
from django.db import models


from cride.utils.models import CrideModel


class Profile(CrideModel):
    """Profile model.
    A profile holds a user's public data like biography, picture,
    and statistics."""

    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name="profile"
        )

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )

    biography = models.TextField(
        max_length=500,
        blank=True
    )

    # Stats
    rides_taken = models.PositiveIntegerField(
        default=0
    )
    rides_offereed = models.PositiveIntegerField(
        default=0
    )

    reputation = models.FloatField(
        default=5,
        help_text="User's reputation based on platform usage."
    )