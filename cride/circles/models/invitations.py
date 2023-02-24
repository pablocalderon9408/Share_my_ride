"""Invitations model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CrideModel

# Managers
from cride.circles.managers.invitations import InvitationManager

class Invitation(CrideModel):
    """Invitation model.

    A invitation is a code that allows a user to join a circle without
    needing an invitation from one of its members.
    """

    code = models.CharField(
        'invitation code',
        max_length=50,
        unique=True,
        blank=True
    )

    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='issued_by'
    )

    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='used_by'
    )

    used = models.BooleanField(
        'used',
        default=False,
        help_text='Set to true when the invitation is used.'
    )

    used_at = models.DateTimeField(blank=True, null=True)

    circle = models.ForeignKey(
        'circles.Circle',
        on_delete=models.CASCADE,
        help_text='Circle to which the invitation belongs.'
    )

    # Managers
    objects = InvitationManager()

    def __str__(self):
        """Return code and circle."""
        return f'Circle: {self.circle.slug_name}, code: {self.code}'

    class Meta(CrideModel.Meta):
        """Meta option."""
        ordering = ['-used', '-created']