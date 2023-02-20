"""Membership model."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CrideModel

class Membership(CrideModel):
    """Membership model.
    
    A membership is the table that holds the relationship between a user and a circle.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    is_admin = models.BooleanField(
        'circle admin',
        default=False,
        help_text='Circle admins can update the circle data and manage its members.'
    )
    
    # Invitations
    used_invitations = models.PositiveIntegerField(default=0)
    remaining_invitations = models.PositiveIntegerField(default=0)
    invited_by = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL, related_name='invited_by')
    
    # Status
    is_active = models.BooleanField(
        'active status',
        default=True,
        help_text='Only active members can interact in the circle.'
    )
    
    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        """Return username and circle."""
        return '@{} at #{}'.format(self.user.username, self.circle.slug_name)
    
    class Meta:
        """Meta option."""
        unique_together = ('user', 'profile', 'circle')