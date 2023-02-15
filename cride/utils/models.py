"""Django models utilities"""


# Django
from django.db import models


class CrideModel(models.Model):
    """Comparte Ride base model.
    CrideModel acts as an abstract base class from which every other model in the project will inherit,
    providing created and modified fields."""

    created = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created"
        )

    modified = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was modified"
        )

    class Meta:

        abstract = True

        get_latest_by = "created"
        ordering = ["-created", "-modified"]
