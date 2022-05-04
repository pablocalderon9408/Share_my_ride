

from django.db import models

from cride.utils.models import CrideModel


class Circle(CrideModel):
    """Circle model.
    
    A circle is a private group where rides are offered and taken 
    by its members. """

    name = models.CharField(
        "circle name",
        max_length=250
    )

    slug_name = models.SlugField(
        unique=True,
        max_length=40
    )

    about = models.CharField(
        "circle description",
        max_length=255
    )

    picture = models.ImageField(
        upload_to="circles/pictures/",
        blank=True,
        null=True
    )

    # Stats
    rides_offered = models.PositiveBigIntegerField(default=0)
    rides_taken = models.PositiveBigIntegerField(default=0)

    verified = models.BooleanField(
        "verified circle",
        default=False,
        help_text="Verified circles are also known as official communities"
    )

    is_public = models.BooleanField(
        help_text="Public circles are listed in the main page.",
        default=True
    )

    is_limited = models.BooleanField(
        "limited",
        default=False,
        help_text="Limited circles can grow to a fixed number of members."
    )

    members_limit = models.PositiveIntegerField(
        default=0,
        help_text="If circle is limited, this will be the limit on the number of members."
    )

    def __str__(self) -> str:
        return self.name

    class Meta(CrideModel.Meta):

        ordering = ["-rides_taken", "-rides_offered"]

